import pymongo.database
from enum import Enum
import json

import ReCompact.dbm.DbObjects.Docs


class ErrorType(Enum):
    DUPLICATE ="duplicate"
class Error(Exception):
    def __init__(self):
        self.inner_exception=None
        self.error_type =None
        """
        Error Type (Loại lỗi)
        see: ReCompact.dbm.db_actions.ErrorType
        """
        self.db_constraint= None
        """
        Db constraint cause error (ràng buộc database phát sinh lỗi)
        """
        self.message = None

        self.data = None
        """
        Data cause error (dữ liệu gây ra lỗi)
        """
        self.fields=None
        """
        Các field gây ra lỗi
        """

def __get_col__(db, data_item_type):
    """
    Get Mongodb Collection base on mongodb model
    :param db:
    :param data_item_type:
    :return:
    """
    assert isinstance(data_item_type, type), f"data_item_type must be a type"
    import pymongo
    coll_name = data_item_type.__meta__.table_name
    coll = db.get_collection(coll_name)
    try:
        if isinstance(data_item_type.__meta__.keys, list):
            for k in data_item_type.__meta__.keys:
                key_name = k
                items = k.split(',')
                indexs = []
                for item in items:
                    indexs.append(
                        (item, pymongo.ASCENDING)
                    )
                coll.create_index(
                    indexs,
                    unique=True
                )
        if isinstance(data_item_type.__meta__.index, list):
            for k in data_item_type.__meta__.index:
                key_name = k
                items = k.split(',')
                indexs = []
                for item in items:
                    indexs.append(
                        (item, pymongo.ASCENDING)
                    )
                coll.create_index(
                    indexs
                )
    finally:
        return coll
    return coll

def __get_all_args_for_insert__(*args, **kwargs):
    import ReCompact.dbm.DbObjects.Docs
    instance = None
    data={}
    if isinstance(args,tuple):
        for v in args:
            if isinstance(v, ReCompact.dbm.DbObjects.Docs.Fields):
                data={**data,**v.to_mongodb()}
            else:
                instance=v

    if not hasattr(instance, "__db__"):
        raise Exception(f"Please set database "
                        f"Thy must call call variable<<db")
    db = getattr(instance, "__db__")
    coll = __get_col__(db, type(instance))
    return db, instance, coll, data,
def __get_all_args_for_find_one__(*args, **kwargs):
    import ReCompact.dbm.DbObjects.Docs
    instance = args[0]
    filter = args[1]
    if isinstance(filter,ReCompact.dbm.DbObjects.Docs.Fields):
        filter = filter.to_mongodb()
    if not hasattr(instance, "__db__"):
        raise Exception(f"Please set database "
                        f"Thy must call call variable<<db")
    db = getattr(instance, "__db__")
    coll = __get_col__(db, type(instance))
    return db, instance, coll, filter
def __get_all_args_for_find__(*args, **kwargs):
    instance = args[0]
    data = args[1]
    if not hasattr(instance, "__db__"):
        raise Exception(f"Please set database "
                        f"Thy must call call variable<<db")
    db = getattr(instance, "__db__")
    coll = __get_col__(db, type(instance))
    return db, instance, coll, data,


def get_all_args_with_filter(*args, **kwargs):
    instance = args[0]
    filter = args[1]
    data = args[2]

    db = getattr(instance, "__db__")
    coll = __get_col__(db, type(instance))
    return db, instance, coll, filter, data


def insert_one(*args, **kwargs):
    db, instance, coll, data = __get_all_args_for_insert__(*args, **kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.insert_one(data)
        data["_id"]=ret._InsertOneResult__inserted_id
        return data

    except pymongo.errors.DuplicateKeyError as e:
        error = Error()
        error.inner_exception = e
        error.message =e._message.split(':')[0]
        error.error_type =ErrorType.DUPLICATE
        str_json= ('{'+e._message.split('{')[1].split('}')[0]+'}').replace('{','{"').replace(': "','": "')
        data_error =json.loads(str_json)
        error.data={}
        for k,v in data_error.items():
            error.data[k.strip(' ')]=v
        error.fields=list(error.data.keys())
        error.db_constraint =e._message.split(':')[1]


        raise error
    except Exception as e:
        error =Error()
        error.inner_exception =e
        raise error



def insert_many(*args, **kwargs):
    # db, instance, coll, data = get_all_args(*args, **kwargs)
    # assert isinstance(coll, pymongo.database.Collection)
    # try:
    #     ret = coll.insert_many(data)
    #     return None, ret
    # except Exception as e:
    #     return e, None
    raise NotImplemented


def update_many(*args, **kwargs):
    db, instance, coll, filter, data = get_all_args_with_filter(*args, **kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.update_many(filter=filter.to_mongodb(),
                               update=data)
        return ret
    except pymongo.errors.DuplicateKeyError as e:
        error = Error()
        error.inner_exception = e
        error.message = e._message.split(':')[0]
        error.error_type = ErrorType.DUPLICATE
        str_json = ('{' + e._message.split('{')[1].split('}')[0] + '}').replace('{', '{"').replace(': "', '": "')
        data_error = json.loads(str_json)
        error.data = {}
        for k, v in data_error.items():
            error.data[k.strip(' ')] = v
        error.fields = list(error.data.keys())
        error.db_constraint = e._message.split(':')[1]

        raise error


def update_one(*args, **kwargs):
    db, instance, coll, filter, data = get_all_args_with_filter(*args, **kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.update_many(filter=filter.to_mongodb(),
                               update=data)
        return data
    except pymongo.errors.DuplicateKeyError as e:
        error = Error()
        error.inner_exception = e
        error.message = e._message.split(':')[0]
        error.error_type = ErrorType.DUPLICATE
        str_json = ('{' + e._message.split('{')[1].split('}')[0] + '}').replace('{', '{"').replace(': "', '": "')
        data_error = json.loads(str_json)
        error.data = {}
        for k, v in data_error.items():
            error.data[k.strip(' ')] = v
        error.fields =list(error.data.keys())
        error.db_constraint = e._message.split(':')[1]

        raise error
    except Exception as e:
        error = Error()
        error.inner_exception = e
        raise error


def delete_many(*args, **kwargs):
    import ReCompact.dbm.DbObjects.Docs
    instance = args[0]
    filter = args[1]
    db = instance.__db__
    cls = type(instance)
    coll = db.get_collection(cls.__meta__.table_name)
    assert isinstance(coll, pymongo.collection.Collection)
    if isinstance(filter, ReCompact.dbm.DbObjects.Docs.Fields):
        filter = filter.to_mongodb()
    ret = coll.delete_many(filter)
    return ret


def delete_one(*args, **kwargs):
    import ReCompact.dbm.DbObjects.Docs
    instance=args[0]
    filter = args[1]
    db= instance.__db__
    cls=type(instance)
    coll = db.get_collection(cls.__meta__.table_name)
    assert isinstance(coll,pymongo.collection.Collection)
    if isinstance(filter,ReCompact.dbm.DbObjects.Docs.Fields):
        filter=filter.to_mongodb()
    ret =coll.delete_one(filter)
    return ret



def find_one(*args, **kwargs):
    db, instance, coll, filter = __get_all_args_for_find_one__(*args, **kwargs)
    assert isinstance(coll,pymongo.collection.Collection)
    return coll.find_one(filter)


def find(*args, **kwargs):
    db, instance, coll, filter = __get_all_args_for_find_one__(*args, **kwargs)
    assert isinstance(coll,pymongo.database.Collection)
    return coll.find(filter)



def __ob_iter__(*args, **kwargs):
    instance = args[0]
    db = instance.__db__
    coll = __get_col__(db, type(instance))
    assert isinstance(coll, pymongo.collection.Collection)
    for x in coll.find({}):
        yield x


def __obj_lshift__(*args, **kwargs):
    if not isinstance(args[1], pymongo.database.Database):
        raise Exception("right argument of left shift must be pymongo.database.Database")
    setattr(args[0], "__db__", args[1])

def __obj_rshift__(*args, **kwargs):
    if not isinstance(args[1], pymongo.database.Database):
        raise Exception("right argument of left shift must be pymongo.database.Database")
    setattr(args[0], "__db__", args[1])

def  __obj_set__(*args,**kwargs):
    import ReCompact.dbm.DbObjects.Docs
    setter = {}
    for x in args:
        if isinstance(x,ReCompact.dbm.DbObjects.Docs.Fields):
            setter ={**setter,**x.to_mongodb()}
        elif isinstance(x,dict):
            setter = {**setter, **x}
    return {"$set":setter}

