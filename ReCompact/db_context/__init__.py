import threading
import threading
import pymongo
import os
import yaml
import gridfs
import bson
import pymongo.database
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

__lock__ = threading.Lock()
__cnn__ = None


def get_db(db_name=None) -> pymongo.database.Database:
    global __cnn__
    global __lock__
    import pymongo
    import web.settings
    if db_name == None:
        db_name = web.settings.DATABASES["default"]["NAME"]
    if __cnn__ == None:
        __lock__.acquire()
        import web.settings
        db_config = web.settings.DATABASES["default"]["CLIENT"]

        __cnn__ = pymongo.mongo_client.MongoClient(
            host=db_config["host"],
            port=db_config["port"],
            username=db_config["username"],
            password=db_config["password"],
            authSource=db_config["authSource"],
            authMechanism=db_config["authMechanism"],
            replicaSet=db_config["replicaSet"]
        )
    return __cnn__.get_database(db_name)


def db_get_gridfs(db: pymongo.database.Database) -> gridfs.GridFS:
    return gridfs.GridFS(db)


def get_mongodb_file_by_file_name(db: pymongo.database.Database, file_name) -> gridfs.grid_file.GridOut:
    """
    Lấy file grid trong mongodb
    """
    return db_get_gridfs(db).find_one({"filename": file_name})


def get_mongodb_file_by_file_id(db: pymongo.database.Database,
                                file_id: bson.objectid.ObjectId) -> gridfs.grid_file.GridOut:
    """
    Lấy file grid trong mongodb với đường dẫn được chỉ định trong path_to_save (bao gồm cả thên file)

    """
    assert isinstance(file_id, bson.objectid.ObjectId), 'id must be pymongo.bson.objectid.ObjectId'
    return db_get_gridfs(db).get(file_id)
