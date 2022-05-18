class __base__:
    def __init__(self):
        self.__fields__={}
def __get_meta__(cls):
    if not hasattr(cls, "__meta__"):
        setattr(cls, "__meta__", __base__())
    return getattr(cls,"__meta__")
def __get_all_fields__(cls):
    ret = {}
    for k,v in cls.__dict__.items():
        if isinstance(v,field):
            ret[v]=v
    return ret
def table(
        table_name,
        keys=None,
        index=None
):
    def ret(cls):
        meta = __get_meta__(cls)
        setattr( meta,"table_name",table_name)
        setattr(meta, "keys", keys)
        setattr(meta, "index", index)
        meta.__fields__ = __get_all_fields__(cls)
        setattr(cls,"__setattr__",__ob_set_attr__)
        fn= getattr(cls,"__getattribute__")
        setattr(cls, "__getattribute__", __ob_get_attr__)
        cls.__original_getattribute__ = fn
        fn_init= getattr(cls,"__init__")
        cls.__ole__init__=fn_init
        setattr(cls,"__init__",__on__init__)
        return cls
    return ret
class field:

    # def __getitem__(self, item):

    def __init__(self,data_type=str,max_len=-1,is_require=False):
        self.data_type=data_type
        self.max_len = max_len
        self.is_require = is_require

def __ob_set_attr__(*args,**kwargs):
    import sys
    instance = args[0]

    cls_type = type(args[0])
    attr_name = args[1]
    attr_value = args[2]
    if not hasattr(cls_type,attr_name):
        raise Exception(f'{cls_type.__module__+"."+cls_type.__name__} do not have property {attr_name}')
    f = getattr(cls_type,attr_name)

    assert isinstance(f,field)
    if attr_value == None and f.is_require==False:
        instance.__dict__["__fields__"]=None

    if f.is_require and attr_value == None:
        raise Exception(f'{cls_type.__module__ + "." + cls_type.__name__}.{attr_name} is require')
    if f.data_type!=type(attr_value):
        raise Exception(f'{cls_type.__module__ + "." + cls_type.__name__}.{attr_name} is must be {f.data_type}')
    if instance.__dict__.get("__fields__",None)==None:
        instance.__dict__["__fields__"]={}
    instance.__dict__["__fields__"][attr_name]=attr_value

def __ob_get_attr__(*args,**kwargs):
    instance = args[0]
    attr_name = args[1]
    assert isinstance(attr_name,str)
    obj_type= type(instance)
    if attr_name.__len__()>4 and attr_name[0:2]=="__" and attr_name[-2:]=="__":
        return obj_type.__original_getattribute__(instance, attr_name)
    if not hasattr(obj_type,attr_name):
        raise Exception(f'{attr_name} was not found in {obj_type.__module__}.{obj_type.__name__}')

    if instance.__dict__.get("__fields__",None)==None:
        instance.__dict__["__fields__"]={}
    return instance.__dict__["__fields__"][attr_name]

def __on__init__(*args,**kwargs):
    if kwargs=={} and args.__len__()>1:
        kwargs=args[1]
        if isinstance(kwargs,dict):
            args[0].__dict__["__fields__"]=args[1]
            return
    instance =args[0]
    cls=type(instance)
    for k,v in kwargs.items():
        if not hasattr(cls,k):
            raise Exception(f'{k} was not found in {cls.__module__}.{cls.__name__}')
        f = getattr(cls,k)
        assert isinstance(f,field)
        if f.is_require and v==None:
            raise Exception(f'{k} in {cls.__module__}.{cls.__name__} is required')
        if v==None:
            instance.__dict__["__fields__"][k]=v
        elif f.data_type!=type(v):
            raise Exception(f'The value {v} set to {k} in {cls.__module__}.{cls.__name__} must be {f.data_type}')
        if not instance.__dict__.get("__fields__",None):
            instance.__dict__["__fields__"]=dict()
        instance.__dict__["__fields__"][k]=v

from  .DbObjects import Docs
FILTER = Docs.Fields()
FIELDS = Docs.Fields()
class SET:
    def __init__(self,*args,**kwargs):
        self.mongo_set ={}
        if isinstance(args,tuple):
            for x in args:
                for k,v in x.to_mongodb().items():
                    self.mongo_set[k]= v
    def to_mongodb(self):
        return {
            "$set":self.mongo_set
        }


