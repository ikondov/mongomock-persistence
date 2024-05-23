# pylint: disable = protected-access
"""patches for the mongomock store classes"""
import os
import collections
import weakref
import bson
from mongomock.thread import RWLock
from mongomock.store import ServerStore, DatabaseStore, CollectionStore


def server_store_init(self, filename=None):
    """replacement for init"""
    self._filename = os.environ.get('MONGOMOCK_SERVERSTORE_FILE', filename)
    if self._filename:
        with open(self._filename, 'r', encoding='utf-8') as fh:
            dct = bson.json_util.loads(fh.read())
        self._databases = {k: DatabaseStore.from_dict(v) for k, v in dct.items()}
        self._finalizer = weakref.finalize(self, self._to_file)
    else:
        self._databases = {}


def server_store_to_dict(self):
    """serialization method"""
    return {k: v.to_dict() for k, v in self._databases.items()}


def server_store_to_file(self):
    """write to file"""
    with open(self._filename, 'w', encoding='utf-8') as fh:
        fh.write(bson.json_util.dumps(self.to_dict()))


ServerStore.__init__ = server_store_init
ServerStore.to_dict = server_store_to_dict
ServerStore._to_file = server_store_to_file


def database_store_init(self, _collections=None):
    """replacement for init"""
    self._collections = _collections or {}


def database_store_to_dict(self):
    """serialization method"""
    return {k: v.to_dict() for k, v in self._collections.items()}


def database_store_from_dict(cls, dct):
    """deserialization method"""
    return cls({k: CollectionStore.from_dict(v) for k, v in dct.items()})


DatabaseStore.__init__ = database_store_init
DatabaseStore.to_dict = database_store_to_dict
DatabaseStore.from_dict = classmethod(database_store_from_dict)


def collection_store_init(self, name, documents=None):
    """replacement for init"""
    self._documents = documents or collections.OrderedDict()
    self.indexes = {}
    self._is_force_created = False
    self.name = name
    self._ttl_indexes = {}

    # 694 - Lock for safely iterating and mutating OrderedDicts
    self._rwlock = RWLock()


def collection_store_to_dict(self):
    """serialization method"""
    return {'name': self.name, 'documents': list(self._documents.items())}


def collection_store_from_dict(cls, dct):
    """deserialization method"""
    return cls(dct['name'], collections.OrderedDict(dct['documents']))


CollectionStore.__init__ = collection_store_init
CollectionStore.to_dict = collection_store_to_dict
CollectionStore.from_dict = classmethod(collection_store_from_dict)
