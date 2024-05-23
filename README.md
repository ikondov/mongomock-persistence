# Mongomock with persistence

This is a package based on the [mongomock](https://github.com/mongomock/mongomock)
package to test any code using MongoDB via the [PyMongo API](https://pymongo.readthedocs.io).

With [mongomock](https://github.com/mongomock/mongomock) the documents are stored in memory and not available after the process performing the tests exits. In some test cases it is necessary to have a non-volatile (persistent) storage of the database. For example, tests of command line interfaces (CLI)  add things into the database and assume they are then available across several processes.

## How it works

This package adds an option to store the database in a file. This is accomplished by small extensions of the classes in `store.py`. These extensions are not intended to keep the database synchronized instantly on disk. Rather the database is eventually dumped to a file only just before the `ServerStore` object is destroyed. After that the file can be used to create other `ServerStore` objects in the final state of the original `ServerStore` object.

## When to use

1. In test cases where a database must be used by several consecutive processes and the database state has to be preserved in the meantimes.

2. In tutorials to learn the basics of using PyMongo-based software.

3. In further single-client applications of MongoDB.

In all use cases one has to make sure that all PyMongo features used are covered by mongomock. See [this](https://github.com/mongomock/mongomock/blob/develop/Missing_Features.rst) for further details.

## How to install

The package can be easily installed using pip:

```
pip install mongomock-persistence
```

## How to use

To use the package the `MongoClient` class from this package must be imported instead of that from [mongomock](https://github.com/mongomock/mongomock). Then the persistence can be activated in two ways:

1. Set the environment variable `MONGOMOCK_SERVERSTORE_FILE` to the name of a non-empty JSON file (initialized with '{}') and call `MongoClient` class as usual:

```
export MONGOMOCK_SERVERSTORE_FILE=/full/path/to/mongomock_file.json
```

```python
from mongomock_persistence import MongoClient
mongo_client = MongoClient()
```

2. Create a custom `ServerStore` object explicitly by using the `filename` keyword argument and then pass it to `MongoClient` call:

```python
from mongomock_persistence import MongoClient
mongo_store = ServerStore(filename='/full/path/to/mongomock_file.json')
mongo_client = MongoClient(_store=mongo_store)
```

## How to test

Install the `test` extra and then run `pytest`, i.e.

```
pip install mongomock-persistence[test]
pytest <root folder of repository>
```
