import sys


def MustImplement():
    """
    Dùng để kiểm tra tính toàn vẹn 1 class và impletementation of class khác
    :return:
    """

    def wrapper(*x, **y):
        __cls__ = x[0]
        __cls__module_path__ = str(sys.modules[__cls__.__module__])
        __base__ = __cls__.__base__
        for k, v in __base__.__dict__.items():
            if (k[0:2] != "__" and k[:-2] != "__") or k=="__init__":
                if callable(v):
                    if __cls__.__dict__.get(k) is None:
                        raise Exception(
                            f"{__cls__.__module__}.{__cls__.__name__}.{k} was not implement in'{__cls__module_path__}' ")

                    v2 = __cls__.__dict__.get(k)
                    if v.__code__.co_argcount != v2.__code__.co_argcount:
                        args = []
                        args2 = []
                        for i in range(0, v.__code__.co_argcount):
                            args += [v.__code__.co_varnames[i]]
                            if i < v2.__code__.co_argcount:
                                args2 += [v2.__code__.co_varnames[i]]

                        raise Exception(

                            f"'{v2.__code__.co_filename}', line {v2.__code__.co_firstlineno}\n"
                            f"see:\n"
                            f"'{v.__code__.co_filename}', line {v.__code__.co_firstlineno} \n"
                            f"\n"
                            f"{__cls__.__module__}.{__cls__.__name__}.{k}({str.join(',', args2)}) but {__base__.__module__}.{__base__.__name__}.{k}({str.join(',', args)})\n "
                            f"")

        return __cls__

    return wrapper
