import yaml
info = None
def init(yaml_config_path:str):
    """
    load yaml info
    Lấy thông tin cài đặt từ file yaml
    :param yaml_config_path:
    :return:
    """
    assert isinstance(yaml_config_path,str),'yaml_config_path mus be str'
    import os
    if not os.path.isfile(yaml_config_path):
        raise FileNotFoundError("'{}' was not found".format(yaml_config_path))
    global info
    with open(yaml_config_path,mode='r',encoding='utf-8') as stream:
        info = yaml.safe_load(stream)
    if not info:
        info = {}
    return True

