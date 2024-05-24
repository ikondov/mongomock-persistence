# pylint: disable = protected-access
"""patch for the mongomock Database class"""
from mongomock import codec_options as mongomock_codec_options
from mongomock.database import ReadConcern, _READ_PREFERENCE_PRIMARY
from mongomock.database import Database


def database_init(self, client, name, _store, read_preference=None, codec_options=None,
                  read_concern=None):
    """replacement for init"""
    self.name = name
    self._client = client
    self._collection_accesses = {}
    self._store = _store or getattr(self._client, '_store')[self.name]
    self._read_preference = read_preference or _READ_PREFERENCE_PRIMARY
    mongomock_codec_options.is_supported(codec_options)
    self._codec_options = codec_options or mongomock_codec_options.CodecOptions()
    if read_concern and not isinstance(read_concern, ReadConcern):
        raise TypeError('read_concern must be an instance of pymongo.read_concern.ReadConcern')
    self._read_concern = read_concern or ReadConcern()


Database.__init__ = database_init
