import pathlib

import yaml
import os
import logging
from fastapi.templating import Jinja2Templates
from .storage.base_storage import base_storage

__logger__ = None

import importlib.util
import sys


# spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
# foo = importlib.util.module_from_spec(spec)
# sys.modules["module.name"] = foo
# spec.loader.exec_module(foo)
# foo.MyClass()


class config_storage:
    """
    Cấu hình nơi lưu trữ
    """

    def __init__(self, config_dir: str, yaml_path, data: dict):

        self.storage_type = data.get('storage_type')
        if self.storage_type is None:
            raise Exception(f"'{self.storage_type}' was not found. Please, preview file '{yaml_path}' at 'temp_dir'")
        current_dir = str(pathlib.Path(__file__).parent)
        path_to_storage_type = os.path.join(current_dir, 'storage', f"{self.storage_type}_storage.py")
        if not os.path.isfile(path_to_storage_type):
            raise FileNotFoundError(f"'{path_to_storage_type}' was not found")
        spec = importlib.util.spec_from_file_location("storage_module", path_to_storage_type)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        class_name = f"{self.storage_type}_storage"
        __cls__ = getattr(module, class_name)
        self.file: base_storage = __cls__(config_dir, yaml_path, data)

        """
        Cấu hình lưu file bằng ổ cứng vật lý hoặc windows share
        """


class config_search:
    """
    Cấu hình Elastic Search
    """

    def __init__(self, config_dir: str, yaml_path, data: dict):
        self.nodes = data.get("nodes")
        """
        Số server node 
        """
        if self.nodes is None:
            raise Exception(f"'nodes' was not found in '{yaml_path}'")
        if not isinstance(self.nodes, list):
            raise Exception(f"'nodes' in '{yaml_path}' is invalid. nodes mus be a list of elastic server nodes")
        self.index = data.get('index')
        """
        Index mặc định
        """
        if self.index is None:
            raise Exception(f"'index' was not found in '{yaml_path}'\n"
                            f"index is the name of index in that content of file was in")
        import ReCompact.es_search
        ReCompact.es_search.set_config(
            self.nodes,
            self.index
        )


class config_broker:
    """
    Lớp cấu hình sử dụng broker server cụ thể là Kafka
    """

    def __init__(self, config_dir: str, broker_yaml_path, data: dict):
        self.enable = data.get("enable", None)
        """
        Chế độ sử dụng kafka. Với những hệ thống kg có xử lý gì phức tạp thì dẹp Kafka qua một bên
        bằng cách đặt bằng False
        """
        if self.enable is None:
            raise Exception(f"'enable' was not found in  '{broker_yaml_path}'")
        self.servers = data.get("servers", None)
        if self.servers is None:
            raise Exception(f"'broker' was not found in  '{broker_yaml_path}'")
        if not isinstance(self.servers, list):
            raise Exception(
                f"'broker' in  '{broker_yaml_path}' is invalid. Broker is a list of node including host:port")
        self.share_directory = data.get('share_directory', None)
        """
        Vì hệ thống có xử lý file nên can62n phải chi sẻ thư mục media
        Điều này có nghĩ là khi upload 1 file bên cạnh việc ghi nhận vào mongosb GridFS
        hệ thống cần file ghi tạm file vào thư mục này
        việc xóa các file này sẽ do 1 tiến trình khác đảm nhiệm
        """
        if self.share_directory is None:
            raise Exception(f"'share_directory' was not found in  '{broker_yaml_path}'")
        if self.share_directory[0:2] == "./":
            """
            Là đường dẫn tương đối chuyển về tuyệt đối
            """
            self.share_directory = os.path.join(config_dir, self.share_directory[2:]).replace('/', os.sep)
            if not os.path.isdir(self.share_directory):
                """
                Trường hợp đường dẫn tương đối mà không có thư mục thì tạo luôn
                Điều này là được phép vì thư mục tạo nằm trong thư mục app
                """
                os.makedirs(self.share_directory)
        else:
            """
            Trường hợp đường dẫn tuyệt đối
            """
            if self.enable:
                """
                Nếu có sử dụng kafka thì phải kiểm tra xem thư mục này có tồn tại hay không
                """
                if not os.path.isdir(self.share_directory):
                    raise Exception(f"'{self.share_directory}' was not found\n"
                                    f"'{self.share_directory}' was use when this system want to send file content to "
                                    f"broker server "
                                    f"If thy would not like to use broker server just set enable in '{broker_yaml_path}' is False")


class config_mongo_db:
    """
    Lớp cấu hình mongodb
    """

    def __init__(self, db_yaml_path, data: dict):
        self.db_yaml_path = db_yaml_path
        self.host = data.get('host', None)
        if self.host is None:
            raise Exception(f"'host' was not found in '{self.db_yaml_path}'")
        self.port = data.get('port', None)
        if self.port is None:
            raise Exception(f"'port' was not found in '{self.db_yaml_path}'")
        self.username = data.get('username', None)
        if self.username is None:
            raise Exception(f"'username' was not found in '{self.db_yaml_path}'")
        self.password = data.get('password', None)
        if self.password is None:
            raise Exception(f"'password' was not found in '{self.db_yaml_path}'")
        self.authSource = data.get('authSource', None)
        if self.authSource is None:
            raise Exception(f"'authSource' was not found in '{self.db_yaml_path}'")
        self.replicaSet = data.get('replicaSet', None)
        if self.replicaSet is None:
            raise Exception(f"'replicaSet' was not found in '{self.db_yaml_path}'")
        self.authMechanism = data.get('authMechanism', None)
        if self.authMechanism is None:
            raise Exception(f"'authMechanism' was not found in '{self.db_yaml_path}'")

    def connection_string(self) -> str:
        ret = f"mongodb://{self.username}:{self.password}"
        host = ""
        if isinstance(self.host, list):
            host = ",".join(self.host)
        else:
            host = f"{self.host}:{self.port}"
        ret += f"@{host}/?authSource={self.authSource}"
        if self.replicaSet != "" and self.replicaSet is not None:
            ret += f"&replicaSet={self.replicaSet}"
        return ret

    def __repr__(self):
        return self.connection_strin()


class config_host_binding:
    """
    Lớp cấu hình host binding
    """

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 8002


class config_host:
    """
    Lớp cấu hình host
    Các thông tin như SSL, tự đông redirect đến SSL đặt ở đây
    """

    def __init__(self):
        self.binding = config_host_binding()
        """
        Binding config
        """


class config_app_jwt:
    def __init__(self, config_yaml_path, data):
        self.secret_key = data.get("secret_key", None)
        if self.secret_key is None:
            raise Exception(f'jwt/secret_key was not found in "{config_yaml_path}"')
        self.algorithm = data.get("algorithm", None)
        if self.algorithm is None:
            raise Exception(f'jwt/algorithm was not found in "{config_yaml_path}"')
        self.access_token_expire_minutes = data.get("access_token_expire_minutes", None)
        if self.access_token_expire_minutes is None:
            raise Exception(f'jwt/access_token_expire_minutes was not found in "{config_yaml_path}"')


class config_app:
    def __init__(self, path_to_config_dir, path_to_yaml_file, data: dict):
        self.path_to_yaml_file = path_to_yaml_file
        """
        Đường dẫn đến file yaml của app
        """
        self.path_to_config_dir = path_to_config_dir
        """
        Đường dẫn đế thư mục của app
        """
        self.temp_upload_dir = data.get("temp_upload_dir", None)
        if self.temp_upload_dir is None:
            raise Exception(f"'temp_upload_dir' was not found in '{path_to_yaml_file}'")
        if self.temp_upload_dir.__len__() > 2 and self.temp_upload_dir[0:2] == "./":
            self.temp_upload_dir = self.temp_upload_dir[2:]
            self.temp_upload_dir = os.path.join(path_to_config_dir, self.temp_upload_dir)
            if not os.path.isdir(self.temp_upload_dir):
                os.makedirs(self.temp_upload_dir)

        self.api = data.get("api", None)
        """
        prefix url from root forapi hosting
        Example: http://localhost:8001/my-api if api is 'my-api'
        """
        if self.api is None:
            raise Exception(f"api was not found in '{self.path_to_yaml_file}'")
        if self.api[0] != '/':
            self.api = '/' + self.api
        self.static = data.get("static", None)
        """
        relative path or absolute path to static resource directory
        """
        if self.static is None:
            raise Exception(f"static was not found in '{self.path_to_yaml_file}'")
        if not os.path.isabs(self.static):
            self.static = os.path.join(self.path_to_config_dir, self.static.replace("./", ""))
        if not os.path.isdir(self.static):
            raise Exception(f"In '{self.path_to_config_dir}'"
                            f"{self.static} was not found\n"
                            f"Thy should preview '{self.path_to_yaml_file} again and check 'static'")
        self.jinja_templates_dir = data.get('jinja_templates_dir', None)
        if self.jinja_templates_dir is None:
            raise Exception(f"'jinja_templates_dir' was not found in '{self.path_to_yaml_file}'")
        if self.jinja_templates_dir.__len__() > 2 and self.jinja_templates_dir[0:2] == "./":
            self.jinja_templates_dir = self.jinja_templates_dir[2:]
            self.jinja_templates_dir = os.path.join(self.path_to_config_dir, self.jinja_templates_dir)
        self.templates = Jinja2Templates(directory=self.jinja_templates_dir)
        """
        Bô render template
        """
        self.root_url = data.get('root_url', None)
        if self.root_url is None:
            raise Exception(f"'root_url' was not found in '{self.path_to_yaml_file}'")
        self.api_url = data.get('api_url', None)
        if self.api_url is None:
            raise Exception(f"'api_url' was not found in '{self.path_to_yaml_file}'")
        jwt_data = data.get("jwt", None)
        if jwt_data is None:
            raise Exception(f"'jwt' was not found in f'{self.path_to_yaml_file}'")
        self.jwt = config_app_jwt(self.path_to_yaml_file, jwt_data)


import traceback


class Config:
    def __init__(self, config_dir: str, logger_name, log_dir=None):
        """
        Init config from config dir
        :param config_dir:
        """

        if not os.path.isdir(config_dir):
            raise Exception(f"'{config_dir}' was not found")

        self.config_dir = config_dir
        if not log_dir:
            self.full_path_to_log = os.path.join(config_dir, "logs").replace('/', os.sep)
            if not os.path.isdir(self.full_path_to_log):
                os.makedirs(self.full_path_to_log, mode=0o777)
        else:
            self.full_path_to_log = log_dir
        self.full_path_to_log = os.path.join(self.full_path_to_log, "log.txt")
        from fastapi.logger import logger
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(name)s : %(message)s')
        file_handler = logging.FileHandler(self.full_path_to_log)
        file_handler.setFormatter(formatter)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        try:
            self.path_to_star_yaml = os.path.join(config_dir, "api_app_start.yaml")
            if not os.path.isfile(self.path_to_star_yaml):
                raise Exception(f"'{self.path_to_star_yaml} was not found")
            self.master_config = self.load_yaml_file(self.path_to_star_yaml)
            self.host_yalm_path = self.master_config.get("host", None)
            if not self.host_yalm_path:
                raise Exception(f"'host' point to host config file was not found in '{self.path_to_star_yaml}'")
            if not os.path.isabs(self.host_yalm_path):
                self.host_yalm_path = os.path.join(self.config_dir, self.host_yalm_path).replace('/', os.sep)
            self.db_yaml_path = self.master_config.get("db", None)
            if not self.db_yaml_path:
                raise Exception(f"'db' point to database config file was not found in '{self.path_to_star_yaml}'")
            if not os.path.isabs(self.db_yaml_path):
                self.db_yaml_path = os.path.join(self.config_dir, self.db_yaml_path).replace('/', os.sep)
            self.app_yaml_path = self.master_config.get("app", None)
            if not self.app_yaml_path:
                raise Exception(f"'app' point to application config file was not found in '{self.path_to_star_yaml}'")
            if not os.path.isabs(self.app_yaml_path):
                self.app_yaml_path = os.path.join(self.config_dir, self.app_yaml_path).replace('/', os.sep)
            self.broker_yaml_path = self.master_config.get("broker", None)
            if self.broker_yaml_path is None:
                raise Exception(
                    f"'broker' point to broker server config file was not found in '{self.path_to_star_yaml}'")
            if not os.path.isabs(self.broker_yaml_path):
                self.broker_yaml_path = os.path.join(self.config_dir, self.broker_yaml_path).replace('/', os.sep)
            self.search_yaml_Path = self.master_config.get("search", None)

            if self.search_yaml_Path is None:
                raise Exception(
                    f"'search' point to broker server config file was not found in '{self.path_to_star_yaml}'")
            if not os.path.isabs(self.search_yaml_Path):
                self.search_yaml_Path = os.path.join(self.config_dir, self.search_yaml_Path).replace('/', os.sep)

            self.storage_yaml_path = self.master_config.get("storage", None)
            if self.storage_yaml_path is None:
                raise Exception(f"'storage' was not found in '{self.path_to_star_yaml}'")

            self.host_dict = self.load_yaml_file(self.host_yalm_path)
            self.db_dict = self.load_yaml_file(self.db_yaml_path)
            self.app_dict = self.load_yaml_file(self.app_yaml_path)
            self.broker_dict = self.load_yaml_file(self.broker_yaml_path)
            self.search_dict = self.load_yaml_file(self.search_yaml_Path)
            self.storage_dict = self.load_yaml_file(self.storage_yaml_path)

            self.storage = config_storage(config_dir, self.storage_yaml_path, self.storage_dict)

            self.host = config_host()
            """
            Host config info
            """
            if self.host_dict.get('binding', None) is None:
                raise Exception(f'binding was not found in "{self.host_yalm_path}"')
            if not isinstance(self.host_dict.get('binding'), dict):
                raise Exception(f'binding in "{self.host_yalm_path}" must have ip attribute and port attribute')

            self.host.binding.ip = self.host_dict["binding"].get("ip", None)
            self.host.binding.port = self.host_dict["binding"].get("port", None)

            if self.host.binding.ip is None:
                raise Exception(f'ip attribute in binding of "{self.host_yalm_path}" was not found')
            if self.host.binding.port is None:
                raise Exception(f'port attribute in binding of "{self.host_yalm_path}" was not found')
            self.mongodb_connection_string = ""
            self.db = config_mongo_db(self.db_yaml_path, self.db_dict)
            self.app = config_app(self.config_dir, self.app_yaml_path, self.app_dict)
            self.broker = config_broker(self.config_dir, self.broker_yaml_path, self.broker_dict)
            self.search = config_search(self.config_dir, self.search_yaml_Path, self.search_dict)
            global __logger__
            __logger__ = self.logger
            self.logger.info("-------------------------")
            self.logger.info(self.host_dict)
            self.logger.info("-------------------------")
            self.logger.info("-------------------------")
            self.logger.info(self.app_dict)
            self.logger.info("-------------------------")
            self.logger.info("-------------------------")
            self.logger.info(self.db_dict)
            self.logger.info("-------------------------")
            self.logger.info("------------------------------------------")
            self.logger.info("------------------------------------------")

        except Exception as e:
            self.logger.debug(traceback.format_exc())
            raise e

    def load_yaml_file(self, yaml_file) -> dict:
        if not os.path.isfile(yaml_file):
            raise FileNotFoundError(f"{yaml_file} was not found")
        with open(yaml_file, mode='r', encoding='utf-8') as stream:
            ret = yaml.safe_load(stream)
        if not ret:
            ret = {}
        return ret
