import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
__lock__ = threading.Lock()
__cnn__= None
def get_db(db_name=None):
    global __cnn__
    global __lock__
    import pymongo
    import web.settings
    if db_name == None:
        db_name = web.settings.DATABASES["default"]["NAME"]
    if __cnn__==None:
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