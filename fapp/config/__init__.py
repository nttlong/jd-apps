"""
Configuration of web app including default value and several setings read form yaml config of web app

"""

import os
import sys
import quicky.yaml_reader
import pathlib
import quicky.logs

debug = True
"""
Debug or release.It will  be overwrite by congfig.yalm 
"""
app_dir = str(pathlib.Path(__file__).parent.parent)
"""
Current directory of web app
Thư mục hiện hành của web app
"""
app_logs_dir = os.path.join(app_dir, "logs")
"""
Biến lưu đường dẫn đến thư mục log
"""
template_folder="templates"
"""
Đường dẫn tương đối đến thư mục template
"""
if not os.path.isdir(app_logs_dir):  # Nếu chưa có thư mục này
    os.makedirs(app_logs_dir)  # Tạo luôn  điều này là chấ nhận được vì app_logs_dir nằm trong app_dir
quicky.logs.set_root_app_dir(app_dir)  # Cài đặt thư mục app cho log
quicky.logs.set_root_dir(app_logs_dir)
logger = quicky.logs.get_logger(__name__, app_dir)

app_config_file = os.path.join(app_dir, "config.yaml")
"""
Đường dẫn đến file cấu hình của tàn bộ app
"""
static_dir = "static"
"""
Đường dẫn đến thư mục static mặc định là static, tuy nhiên vẫn có thề điều chỉnh lại trong file congfig.yaml
"""
static_url="/static"
"""
url gốc để truy cập static directory
"""
__full_static_dir__ = os.path.join(app_dir, static_dir)

__full_template_path__= os.path.join(app_dir,template_folder)

def get_full_static_dir():
    """
    Get full path to static directory
    :return:
    """
    global __full_static_dir__
    return __full_static_dir__

def get_full_template_dir():
    """
    Lấy đường dẫn đến thư mục template
    :return:
    """
    global __full_template_path__
    return __full_static_dir__

if not os.path.isdir(__full_static_dir__):
    os.makedirs(__full_static_dir__)
if not os.path.isdir(__full_template_path__):
    os.makedirs(__full_template_path__)
if not os.path.isfile(app_config_file):
    logger.debug(f'{app_config_file} was not found')
    raise FileNotFoundError(f"{app_config_file} was not found")

host = "192.168.1.2"
"""
host of web app.It will  be overwrite by congfig.yalm
"""
port = "5432"
"""
port of web app. It will be overwrite by config.yaml
"""
current_module = sys.modules[__name__]
"""
module config
"""
__config__ = quicky.yaml_reader.from_file(app_config_file)
try:
    for k, v in __config__.items():
        if k == "static":
            if os.path.isabs(v):
                if not os.path.isdir(v):
                    exception_msg = f"'{v}' was not found " \
                                    f"Thy should check static in '{app_config_file}'"
                    logger.info(exception_msg)
                    raise Exception(exception_msg)
                __full_static_dir__ = v
            else:
                __full_static_dir__ = os.path.join(app_dir, v)
                if not os.path.isdir(__full_static_dir__):
                    os.makedirs(__full_static_dir__)
        if k=="template_folder":
            if os.path.isabs(v):
                if not os.path.isdir(v):
                    exception_msg = f"'{v}' was not found " \
                                    f"Thy should check template_folder in '{app_config_file}'"
                    logger.info(exception_msg)
                    raise Exception(exception_msg)
                __full_template_path__ =v
            else:
                __full_template_path__ = os.path.join(app_dir, v)
                if not os.path.isdir(__full_template_path__):
                    os.makedirs(__full_template_path__)
        elif hasattr(current_module, k):
            setattr(current_module, k, v)
except Exception as e:
    logger.debug(e)
    raise e

"""
Apply settings  from yaml.config
"""
logger.info(f"load settings was sucessfull")
logger.info(f"-----------------------------------")

logger.info(__config__)
logger.info(f"-----------------------------------")
