import pymongo.collection


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

class Aggregate:
    def __init__(self,*args,**kwargs):
        instance =args[0]
        self.db = instance.__db__
        self.cls = type(instance)
        self.collection_name = type(instance).__meta__.table_name
        self.pipeline=[]
    def __repr__(self):
        import json
        return json.dumps(self.pipeline)
    def match(self,filter):
        import ReCompact.dbm.DbObjects.Docs
        if isinstance(filter,ReCompact.dbm.DbObjects.Docs.Fields):
            self.pipeline+=[{"$match":filter.to_mongodb()}]
        elif isinstance(filter,dict):
            self.pipeline += [{"$match":filter}]
        else:
            raise Exception("match must be call with ReCompact.dbm.DbObjects.Docs.Fields or dict")
        return self
    @property
    def fields(self):
        import ReCompact.dbm.DbObjects.Docs
        return ReCompact.dbm.DbObjects.Docs.Fields
    def project(self,*args,**kwargs):
        import ReCompact.dbm.DbObjects.Docs
        a = {}
        if isinstance(args,tuple):
            for x in args:
                if isinstance(x,ReCompact.dbm.DbObjects.Docs.Fields):
                    a[x.to_mongodb()]=1
                elif isinstance(x,str):
                    a[x] = 1
        if isinstance(kwargs,dict):
            for k,v in kwargs.items():
                if isinstance(v,ReCompact.dbm.DbObjects.Docs.Fields):
                    a[k]=v.to_mongodb()
                elif isinstance(x,str):
                    a[x] = 1

        self.pipeline+=[{"$project":a}]
        return self
    def sort(self,*args,**kwargs):
        import ReCompact.dbm.DbObjects.Docs
        a={}
        if isinstance(args,tuple):
           for v in args:
               if isinstance(v,dict):
                   a = {**a, **v}
        self.pipeline+=[{"$sort":a}]

        return self
    def __iter__(self):
        coll =__get_col__(self.db,self.cls)
        assert isinstance(coll,pymongo.collection.Collection)
        ret =coll.aggregate(self.pipeline)
        return ret
