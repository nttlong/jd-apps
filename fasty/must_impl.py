"""
Declare class wrapper function.
any sub class was wrapper with must_implement have to implement
any method with the same params of parent class
"""


def must_implement(*x, **y):
    def wrapper(*args, **kwargs):
        cls = args[0]
        if isinstance(cls, type):
            base_cls = cls.__base__
            for k, v in base_cls.__dict__.items():
                if ((k[0:2] != "__" and k[:-2] != "__") or k == "__init__") and callable(v):
                    cls_method = cls.__dict__.get(k, None)
                    if cls_method is None:
                        raise Exception(f"{base_cls}.{k} was not implement in {cls}"
                                        f"")
                    if not callable(cls_method):
                        raise Exception(f"{cls}.{k} must be a method like {cls}.{k}"
                                        f"see:"
                                        f"")
                    base_args = []
                    cls_args = []
                    num_of_args = v.__code__.co_argcount
                    for i in range(0, num_of_args):
                        base_args += [v.__code__.co_varnames[i]]
                        if i < cls_method.__code__.co_argcount:
                            cls_args += [cls_method.__code__.co_varnames[i]]
                    str_base_method = ",".join(base_args)
                    str_cls_method = ",".join(cls_args)
                    if str_cls_method!= str_base_method:
                        raise Exception(f"{base_cls}.{k}({str_base_method}) \n whilst {cls}.{str_cls_method}"
                                        f"\nsee:\n "
                                        f"'{cls_method.__code__.co_filename}', line {cls_method.__code__.co_firstlineno }"
                                        f"\nref from :\n "
                                        f"'{v.__code__.co_filename}', line {v.__code__.co_firstlineno }")


            return cls

    return wrapper


