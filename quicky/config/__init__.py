import logging
import os
import pathlib
from .. import logs
from .. import yaml_reader
from .. import logs
class Config:
    def __init__(self,app_file:str):
        if not os.path.isfile(app_file):
            raise Exception(f"{app_file} was not found")
        """
        Create config form app_dir
        :param app_dir:
        """
        self.host_dir='/'
        self.debug = True
        self.host = "127.0.0.1"
        self.port =5432
        """
        Debug or release.It will  be overwrite by congfig.yalm
        """
        self.app_dir = str(pathlib.Path(app_file).parent.parent)
        """
        Current directory of web app
        Thư mục hiện hành của web app
        """
        self.app_logs_dir = os.path.join(self.app_dir, "logs")

        """
        Biến lưu đường dẫn đến thư mục log đường dẫn đầy đủ
        """
        self.template_folder = "templates"
        """
        Đường dẫn tương đối đến thư mục template
        """
        self.app_config_file = os.path.join(self.app_dir, "config.yaml")
        """
        Đường dẫn đến file cấu hình của tàn bộ app
        """
        if not os.path.isfile(self.app_config_file):
            raise FileNotFoundError(f"{self.app_config_file} was not found")
        self.static_dir = "static"
        """
        Đường dẫn đến thư mục static mặc định là static, tuy nhiên vẫn có thề điều chỉnh lại trong file congfig.yaml
        """
        self.static_url = "/static"
        """
        url gốc để truy cập static directory
        """
        self.full_static_dir = os.path.join(self.app_dir, self.static_dir)
        """
        Đường dẫn đầy đủ đến thư mục static
        """

        self.full_template_path = os.path.join(self.app_dir, self.template_folder)
        """
        Đường dẫn đầy đủ đến thư mục template
        """
        self.check_all_folder()
        self.logger = self.get_loger(__name__)
        self.load_yaml_config()
    def get_loger(self,name)->logging.Logger:
        logs.set_root_app_dir(self.app_dir)  # Cài đặt thư mục app cho log
        logs.set_root_dir(self.app_logs_dir)
        logger = logs.get_logger(name, self.app_dir)
        return logger
    def create_folder_if_not_exist(self,folder_path):
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
    def check_all_folder(self):
        """
        Kiểm tra các thư mục cần thiết. nếu thiếu thì tạo
        :return:
        """
        self.create_folder_if_not_exist(self.full_template_path)
        self.create_folder_if_not_exist(self.app_logs_dir)
        self.create_folder_if_not_exist(self.static_dir)
    def load_yaml_config(self):
        """
        Lấy thông tin từ file yaml và cài đặt lại các tham số
        :return:
        """
        try:
            self.meta = yaml_reader.from_file(self.app_config_file)
            for k,v in self.meta.items():
                if k == "static":
                    if os.path.isabs(v):
                        if not os.path.isdir(v):
                            exception_msg = f"'{v}' was not found " \
                                            f"Thy should check static in '{self.app_config_file}'"

                            raise Exception(exception_msg)
                        __full_static_dir__ = v
                    else:
                        __full_static_dir__ = os.path.join(self.app_dir, v)
                        if not os.path.isdir(__full_static_dir__):
                            os.makedirs(__full_static_dir__)
                if k == "template_folder":
                    if os.path.isabs(v):
                        if not os.path.isdir(v):
                            exception_msg = f"'{v}' was not found " \
                                            f"Thy should check template_folder in '{ self.app_config_file}'"

                            raise Exception(exception_msg)
                        self.full_template_path = v
                    else:
                        self.full_template_path = os.path.join(self.app_dir, v)
                        if not os.path.isdir(self.full_template_path):
                            os.makedirs(self.full_template_path)

                if hasattr(self,k):
                    setattr(self,k,v)
        except Exception as e:
            self.logger.info(exception_msg)
            raise e
    def get_route_path(self, r_path):

        if self.host_dir != '/' and self.sub_dir.__len__() > 1:
            if self.host_dir[0:1] != '/':
                raise Exception(f"{self.sub_dir} must start with '/")
            return self.host_dir + r_path
        else:
            return r_path









