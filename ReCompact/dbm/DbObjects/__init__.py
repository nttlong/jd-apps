import asyncio
def __get_col__(db, data_item_type):
    import pymongo
    coll_name = data_item_type.__meta__.table_name
    coll = db.get_collection(coll_name)
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
    return coll
def insert(db, data_item):
    import pymongo
    assert isinstance(db, pymongo.mongo_client.database.Database),'db must be pymongo.mongo_client.database'
    data_item_type = type(data_item)
    coll = __get_col__(db,data_item_type)
    coll.insert(data_item.__dict__["__fields__"])
def find_to_objects(db,data_item_type,filter):
    import pymongo
    assert isinstance(db,pymongo.mongo_client.database.Database),f'db must be pymongo.mongo_client.database.Database'
    assert isinstance(filter,Docs.Fields), 'filter must be ReCompact.dbm.DbObject.Filter'
    coll= __get_col__(db,data_item_type)
    ret = coll.find(filter.to_mongodb())
    for x in list(ret):
        yield data_item_type(x)
async def find_to_objects_async(db,data_item_type,filter):
    import pymongo
    assert isinstance(db, pymongo.mongo_client.database.Database), f'db must be pymongo.mongo_client.database.Database'
    assert isinstance(filter, Docs.Fields), 'filter must be ReCompact.dbm.DbObject.Filter'
    coll = __get_col__(db, data_item_type)
    ret = coll.find(filter.to_mongodb())
    for x in list(ret):
        yield data_item_type(x)

def find_to_object(db,data_item_type,filter):
    import pymongo
    assert isinstance(db,pymongo.mongo_client.database.Database),f'db must be pymongo.mongo_client.database.Database'
    assert isinstance(filter,Docs.Fields), 'filter must be ReCompact.dbm.DbObject.Filter'
    coll= __get_col__(db,data_item_type)
    ret = coll.find_one(filter.to_mongodb())
    return data_item_type(ret)
def find_to_dict(db,data_item_type,filter):
    import pymongo
    assert isinstance(db,pymongo.mongo_client.database.Database),f'db must be pymongo.mongo_client.database.Database'
    assert isinstance(filter,Docs.Fields), 'filter must be ReCompact.dbm.DbObject.Filter'
    coll= __get_col__(db,data_item_type)
    return coll.find(filter.to_mongodb())


def find_one_to_dict(db,data_item_type,filter):
    import pymongo
    assert isinstance(db,pymongo.mongo_client.database.Database),f'db must be pymongo.mongo_client.database.Database'
    assert isinstance(filter,Docs.Fields), 'filter must be ReCompact.dbm.DbObject.Filter'
    coll= __get_col__(db,data_item_type)
    return coll.find_one(filter.to_mongodb())

def aggregrate(db,object_type):
    return  Aggregrate(db,object_type)

from . import Docs
Filter = Docs.Fields()

class Aggregrate:
    def __init__(self,db,object_type):
        self.db = db
        self.object_type= object_type
        self.mongo_collection= __get_col__(db,object_type)
        self.pipeline=[]
    def __iter__(self):
        ret =self.mongo_collection.aggregate(self.pipeline)
        return ret

