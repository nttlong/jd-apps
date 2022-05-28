"""
Configuration of web app including default value and several setings read form yaml config of web app

"""

import os
import sys
import quicky.yaml_reader
import pathlib
import quicky.logs
debug= True
"""
Debug or release.It will  be overwrite by congfig.yalm 
"""
app_dir = str(pathlib.Path(__file__).parent.parent)
"""
Current directory of web app
Thư mục hiện hành của web app
"""
app_logs_dir = os.path.join(app_dir,"logs")
"""
Biến lưu đường dẫn đến thư mục log
"""
if not os.path.isdir(app_logs_dir): # Nếu chưa có thư mục này
    os.makedirs(app_logs_dir) # Tạo luôn  điều này là chấ nhận được vì app_logs_dir nằm trong app_dir
quicky.logs.set_root_app_dir(app_dir) # Cài đặt thư mục app cho log
quicky.logs.set_root_dir(app_logs_dir)
logger = quicky.logs.get_logger(__name__,app_dir)


app_config_file = os.path.join(app_dir,"config.yaml")
"""
Đường dẫn đến file cấu hình của tàn bộ app
"""
if not os.path.isfile(app_config_file):
    logger.debug(f'{app_config_file} was not found')
    raise FileNotFoundError(f"{app_config_file} was not found")

host="192.168.1.2"
"""
host of web app.It will  be overwrite by congfig.yalm
"""
port="5432"
"""
port of web app. It will be overwrite by config.yaml
"""
current_module = sys.modules[__name__]
"""
module config
"""
__config__ = quicky.yaml_reader.from_file(app_config_file)
try:
    for k,v in __config__.items():
        if hasattr(current_module,k):
            setattr(current_module,k,v)
except Exception as e:
    logger.debug(e)
    raise e


"""
Apply settings  from yaml.config
"""
logger.info(f"load settings was sucessfull")
logger.info(f"-----------------------------------")

logger.info(current_module.__dict__)
logger.info(f"-----------------------------------")

