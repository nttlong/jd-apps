import pymongo.database


def __get_col__(db, data_item_type):
    """
    Get Mongodb Collection base on mongodb model
    :param db:
    :param data_item_type:
    :return:
    """
    assert isinstance(data_item_type,type),f"data_item_type must be a type"
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

def get_all_args(*args,**kwargs):
    instance = args[0]
    data = args[1]
    db = getattr(instance, "__db__")
    coll = __get_col__(db,type(instance))
    return db,instance,coll,data,
def get_all_args_with_filter(*args,**kwargs):
    instance = args[0]
    filter = args[1]
    data = args[1]
    db = getattr(instance, "__db__")
    coll = __get_col__(db,type(instance))
    return db,instance,coll,filter,data

def insert_one(*args,**kwargs):
    db,instance,coll,data = get_all_args(*args,**kwargs)
    assert isinstance(coll,pymongo.database.Collection)
    try:
        ret = coll.insert_one(data)
        return None,ret
    except Exception as e:
        return e, None
def insert_many(*args,**kwargs):
    db,instance,coll,data = get_all_args(*args,**kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.insert_many(data)
        return None, ret
    except Exception as e:
        return e, None
def update_many(*args,**kwargs):
    db,instance,coll,filter,data=get_all_args_with_filter(*args,**kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.update_many(filter=filter.to_mongodb(),
                               update=data)
        return None, ret
    except Exception as e:
        return e, None

def update_one(*args,**kwargs):
    db,instance,coll,filter,data=get_all_args_with_filter(*args,**kwargs)
    assert isinstance(coll, pymongo.database.Collection)
    try:
        ret = coll.update_many(filter=filter.to_mongodb(),
                               update=data)
        return None, ret
    except Exception as e:
        return e, None

def delete_many(*args,**kwargs):
    db,instance,coll,filter,data=get_all_args_with_filter(*args,**kwargs)
    raise NotImplemented()

def delete_one(*args,**kwargs):
    db,instance,coll,filter,data=get_all_args_with_filter(*args,**kwargs)
    raise NotImplemented()

def find_one(*args,**kwargs):
    db, instance, data = get_all_args(*args, **kwargs)
    raise NotImplemented()

def find(*args,**kwargs):
    db, instance, data = get_all_args(*args, **kwargs)
    raise NotImplemented()