import datetime

import bson
import motor.motor_asyncio
import pymongo
import asyncio
import ReCompact.dbm
import ReCompact.dbm.DbObjects.Docs
import threading
import enum
import quicky.yaml_reader
import pathlib
import os
import pymongo.mongo_client

__lock__ = threading.Lock()
__cache_index_creator__ = {}
__connection__ = None
db_config = None
default_db_name = None
connection_string = None


def load_config(path_to_yalm_database_config):
    global default_db_name
    global db_config
    global connection_string
    global __connection__
    if not os.path.isfile(path_to_yalm_database_config):
        raise Exception(f"'{path_to_yalm_database_config}' was not found")

    db_config = quicky.yaml_reader.from_file(path_to_yalm_database_config)
    default_db_name = db_config["authSource"]
    str_auth = f'{db_config["username"]}:{db_config["password"]}'
    str_host = None
    if isinstance(db_config["host"], list):
        str_host = ",".join(db_config["host"])
    elif isinstance(db_config["host"], str):
        str_host = f'{db_config["host"]}:{db_config["port"]}'
    if db_config.get("replicaSet", None) is not None:
        connection_string = f'mongodb://{db_config["username"]}:{db_config["password"]}@{str_host}/?authSource={db_config["authSource"]}&replicaSet={db_config["replicaSet"]}'
        __connection__ = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
    else:
        connection_string = f'mongodb://{db_config["username"]}:{db_config["password"]}@{str_host}/?authSource={db_config["authSource"]}'
        __connection__ = motor.motor_asyncio.AsyncIOMotorClient(connection_string)


class ErrorType(enum.Enum):
    NONE = "None"
    DUPLICATE_DATA = "DuplicateData"
    SYSTEM = "system"


class Error(Exception):
    def __init__(self):
        self.code = ErrorType.NONE
        self.message = ""
        self.fields = []
        self.key_values = {}
        self.inner_exception = None


def __parse_error__(ex):
    ret = Error()
    if isinstance(ex, pymongo.errors.DuplicateKeyError):
        keyPattern = ex.details.get('keyPattern')
        keyValue = ex.details.get('keyValue')
        fields = list(keyPattern.keys())
        ret.inner_exception = ex
        ret.fields = fields
        ret.key_values = keyValue
        ret.fields = fields
        return ret
    elif isinstance(ex, Exception):
        ret.code = ErrorType.SYSTEM
        ret.message = "system error see inner"
        return ret


def __set_connection__(db):
    global __connection__
    global __lock__
    if __connection__ is None:
        __lock__.acquire()
        try:
            if isinstance(db, pymongo.mongo_client.database.Database):
                username = db.client.options._options["username"]
                password = db.client.options._options["password"]
                replicaSet = db.client.options._options.get("replicaSet", None)
                authSource = db.client.options._options["authSource"]
                # host = list(db.client.HOST)
                str_host = ",".join([f"{x[0]}:{x[1]}" for x in list(db.client.nodes)])
                uri = f'mongodb://{username}:{password}@{str_host}/?authSource={authSource}'
                if replicaSet is not None:
                    uri = f'mongodb://{username}:{password}@{str_host}/?replicaSet={replicaSet}&authSource={authSource}'
                __connection__ = motor.motor_asyncio.AsyncIOMotorClient(uri)
        except Exception as e:
            raise e
        finally:
            __lock__.release()
    return getattr(__connection__, db.name)


def __fix_bson_object_id__(fx):
    ret = {}
    for k, v in fx.items():
        if isinstance(v, bson.ObjectId):
            ret = {**ret, **{k: {"$oid": str(v)}}}

        elif isinstance(v, dict):
            ret = {**ret, **{k: __fix_bson_object_id__(v)}}
        elif isinstance(v, list):
            lst = list(__fix_bson_object_id_in_list__(v))
            ret = {**ret, **{k: lst}}
        else:
            ret = {**ret, **{k: v}}
    return ret


def __fix_bson_object_id_in_list__(fx):
    lst = []
    for x in fx:
        ret = __fix_bson_object_id__(x)
        yield ret


async def __get_collection__(db, collection_name, keys, index):
    coll = getattr(db, collection_name)
    global __cache_index_creator__
    global __lock__
    key = f"{db.name}/{collection_name}".lower()

    if not __cache_index_creator__.get(key, None):
        __lock__.acquire()
        try:
            index_info = await coll.index_information()

            async def check(key):
                set_key = set(key)
                for k, v in index_info.items():
                    set_key_in_db = set([x[0] for x in v.get('key')])
                    if len(set_key_in_db & set_key) > 0:
                        return True
                return False

            if isinstance(keys, list):
                for k in keys:
                    key_name = k
                    items = k.split(',')
                    is_already = await check(items)
                    if is_already:
                        continue
                    indexs = []
                    partialFilterExpression_dict = {}
                    for item in items:
                        indexs.append(
                            (item, pymongo.ASCENDING)
                        )
                        partialFilterExpression_dict = {
                            **partialFilterExpression_dict,
                            **{
                                item: {
                                    "$exists": None
                                }
                            }

                        }
                    try:

                        coll.create_index(
                            indexs,
                            unique=True,
                            sparse=True,
                            # partialFilterExpression =partialFilterExpression_dict,
                            background=True
                        )
                    except:
                        pass
                    finally:
                        pass

            if isinstance(index, list):
                for k in index:
                    key_name = k
                    items = k.split(',')
                    is_already = await check(items)
                    if is_already:
                        continue
                    indexs = []
                    for item in items:
                        indexs.append(
                            (item, pymongo.ASCENDING)
                        )
                    try:
                        coll.create_index(
                            indexs,
                            background=True
                        )
                    except:
                        pass
                    finally:
                        pass
        finally:
            __cache_index_creator__[key] = key
            __lock__.release()
            return coll

    return coll


async def find_one_async(db: motor.motor_asyncio.AsyncIOMotorDatabase, docs, filter=None):
    """

    :param db:
    :param docs:
    :param filter:
    :return:
    """
    async_db = __set_connection__(db)
    coll = await __get_collection__(
        async_db,
        docs.__dict__["__collection_name__"],
        docs.__dict__["__collection_keys__"],
        docs.__dict__["__collection_index__"]
    )
    if filter is None:
        filter = {}
    _filter = filter
    if isinstance(filter, ReCompact.dbm.DbObjects.Docs.Fields):
        _filter = filter.to_mongodb()
    ret = await coll.find_one(_filter)
    ret_dict = __fix_bson_object_id__(ret)
    return ret_dict


def find_one(db: motor.motor_asyncio.AsyncIOMotorDatabase, docs, filter=None):
    ret = sync(find_one_async(db, docs, filter))
    return ret


async def find_async(db: motor.motor_asyncio.AsyncIOMotorDatabase,
                     docs,
                     filter=None,
                     skip=0,
                     limit=100):
    """

        :param db:
        :param docs:
        :param filter:
        :return:
        """
    async_db = __set_connection__(db)

    coll = await __get_collection__(
        async_db,
        docs.__dict__["__collection_name__"],
        docs.__dict__["__collection_keys__"],
        docs.__dict__["__collection_index__"]
    )

    _filter = filter
    if isinstance(filter, ReCompact.dbm.DbObjects.Docs.Fields):
        _filter = filter.to_mongodb()
    ret_cursor = coll.find(_filter)
    ret = await ret_cursor.skip(skip).to_list(limit)
    lst = list(__fix_bson_object_id_in_list__(ret))
    return lst


def find(db, docs,
         filter=None,
         skip=0,
         limit=100):
    ret = sync(find_async(db, docs, filter, skip, limit))
    return ret


async def delete_many_async(db, docs, filter):
    async_db = __set_connection__(db)
    coll = await __get_collection__(
        async_db,
        docs.__dict__["__collection_name__"],
        docs.__dict__["__collection_keys__"],
        docs.__dict__["__collection_index__"]
    )
    assert isinstance(coll, motor.motor_asyncio.AsyncIOMotorCollection)
    _filter = {}
    if isinstance(filter, ReCompact.dbm.Docs.Fields):
        _filter = filter.to_mongodb()
    elif isinstance(filter, dict):
        _filter = filter
    else:
        raise Exception("filter must be ReCompact.dbm.Docs.Fields or dict")
    ret = await coll.delete_many(_filter)
    return ret


def delete_many(db, docs, filter):
    return sync(delete_many_async(db, docs, filter))


async def delete_one_async(db, docs, filter):
    async_db = __set_connection__(db)
    coll = await __get_collection__(
        async_db,
        docs.__dict__["__collection_name__"],
        docs.__dict__["__collection_keys__"],
        docs.__dict__["__collection_index__"]
    )
    assert isinstance(coll, motor.motor_asyncio.AsyncIOMotorCollection)
    _filter = {}
    if isinstance(filter, ReCompact.dbm.Docs.Fields):
        _filter = filter.to_mongodb()
    elif isinstance(filter, dict):
        _filter = filter
    else:
        raise Exception("filter must be ReCompact.dbm.Docs.Fields or dict")
    ret = await coll.delete_one(_filter)
    return ret


def delete_one(db, docs, filter):
    return sync(delete_one_async(db, docs, filter))


async def insert_one_async(db, docs, *args, **kwargs):
    try:
        async_db = __set_connection__(db)
        coll = await __get_collection__(
            async_db,
            docs.__dict__["__collection_name__"],
            docs.__dict__["__collection_keys__"],
            docs.__dict__["__collection_index__"]
        )
        assert isinstance(coll, motor.motor_asyncio.AsyncIOMotorCollection)
        data = {}
        if isinstance(args, tuple) and len(args) > 0:
            for x in args:
                if isinstance(x, dict):
                    data = {**data, **x}
                elif isinstance(x, ReCompact.dbm.Docs.Fields):
                    data = {**data, **x.to_mongodb()}

        ret = await coll.insert_one(data)
        data["_id"] = ret.inserted_id
        return data
    except pymongo.errors.DuplicateKeyError as e:
        r_e = __parse_error__(e)
        raise r_e
    except Exception as e:
        raise e


def insert_one(db, docs, *args, **kwargs):
    ret = sync(insert_one_async(db, docs, *args, **kwargs))
    return ret


async def update_one_async(db, docs, filter, *args, **kwargs):
    try:
        async_db = __set_connection__(db)
        coll = await __get_collection__(
            async_db,
            docs.__dict__["__collection_name__"],
            docs.__dict__["__collection_keys__"],
            docs.__dict__["__collection_index__"]
        )
        assert isinstance(coll, motor.motor_asyncio.AsyncIOMotorCollection)
        data = {}
        _filter = {}
        if isinstance(filter, dict):
            _filter = filter
        elif isinstance(filter, ReCompact.dbm.Docs.Fields):
            _filter = filter.to_mongodb()
        else:
            raise Exception("filter of db_asycn.update_one_async or db_asycn.update_one \n"
                            "must be ReCompact.dbm.Docs.Fields or dict\n"
                            "Example:\n"
                            "update_one_async(db,docs,docs._id=='x',docs.Code=='aa')")
        if isinstance(args, tuple):
            for x in args:
                if isinstance(x, dict):
                    data = {**data, **x}
                elif isinstance(x, ReCompact.dbm.Docs.Fields):
                    data = {**data, **x.to_mongodb()}
                elif isinstance(x, tuple):
                    for y in x:
                        if isinstance(y, dict):
                            data = {**data, **y}
                        elif isinstance(x, ReCompact.dbm.Docs.Fields):
                            data = {**data, **y.to_mongodb()}

        ret = await coll.update_one(data)
        data["_id"] = ret.inserted_id
        return data
    except pymongo.errors.DuplicateKeyError as e:
        r_e = __parse_error__(e)
        raise r_e
    except Exception as e:
        raise e


def update_one(db, docs, filter, *args, **kwargs):
    return sync(update_one_async(db, docs, filter, *args, **kwargs))


def sync(*args, **kwargs):
    """
    Khử sync
    :param args:
    :param kwargs:
    :return:
    """
    loop = asyncio.get_event_loop()
    coroutine = args[0]
    ret = loop.run_until_complete(coroutine)
    return ret


def get_connection() -> motor.motor_asyncio.AsyncIOMotorClient:
    global __connection__
    if __connection__ is None:
        raise Exception(f"Thy shoul call Recompact.db_async.load_config")
    return __connection__


__all_instances_db_context__ = {}
__mongo_db_instance__ = {}
__lock_2__ = threading.Lock()


class DbContext:
    def __init__(self, db_name):
        cnn = get_connection()
        self.db = getattr(cnn, db_name)

    async def find_one_async(self, docs, filter):
        ret = await find_one_async(self.db, docs, filter)
        return ret

    def find_one(self, docs, filter):
        return sync(self.find_one_async(docs, filter))

    async def find_async(self, docs, filter, skip=0, limit=100):
        ret = await find_async(self.db, docs, filter, skip, limit)
        return ret

    def find(self, docs, filter, skip=0, limit=100):
        return sync(self.find_async(docs, filter, skip, limit))


def get_db_context(db_name) -> DbContext:
    global __all_instances_db_context__
    global __lock_2__
    if __all_instances_db_context__.get(db_name, None) is None:
        __lock_2__.acquire()
        try:
            cntx = DbContext(db_name)
            __all_instances_db_context__[db_name] = cntx
        finally:
            __lock_2__.release()
    return __all_instances_db_context__[db_name]
