import flask
from flask_restful import Resource, Api
from . import config

__app__ = None
__api_dir__ = '/api'


class QuickyApp(flask.app.Flask):
    def __init__(self, name, app_config: config.Config):
        super().__init__(
            name,
            static_folder=app_config.full_static_dir,
            static_url_path=app_config.static_url,
            template_folder=app_config.full_template_path
        )
        self.app_config = app_config
        self.api = Api(self)
        global __app__
        __app__ = self


def set_api_die(path):
    global __api_dir__
    __api_dir__ = path


def get_app() -> QuickyApp:
    global __app__
    return __app__


def api_add_resource(controller_class, url_path: str):
    """
    Thêm Api resourece
    :param controller_class: phải là một class thừa kế từ flask_restful.Resource
    :param url_path:
    :return:
    """
    if not url_path.startswith('/'):
        raise Exception(f"'{url_path}' must start with '/")
    if not isinstance(controller_class, type) and not issubclass(controller_class,Resource):
        raise Exception(
            f"{controller_class.__module__}.{controller_class.__name__} must inherit from {Resource.__module__}.{Resource.__name__}")
    global __api_dir__
    if __api_dir__ == '/':
        get_app().api.add_resource(controller_class, get_app().app_config.get_route_path(url_path))
    else:
        get_app().api.add_resource(controller_class, get_app().app_config.get_route_path(__api_dir__ + url_path))


def add_api_handler(path, handler, endpoint, methods=['GET']):
    """
    Thêm 1 api handler, có nghĩa là không dùng Api Objet mà dùng hàm
    :param path:
    :param handler:
    :param endpoint:
    :param methods:
    :return:
    """
    if path[0]!='/':
        raise Exception(f"'{path}' must start with /")
    if not callable(handler):
        raise Exception(
            f"{handler.__module__}.{handler.__name__} must be a function")
    global __api_dir__
    if __api_dir__ == '/':
        get_app().add_url_rule(get_app().app_config.get_route_path(path), endpoint, handler, methods)
    else:
        get_app().add_url_rule(get_app().app_config.get_route_path(__api_dir__ + path), endpoint, handler, methods)


def add_handler(path, handler, endpoint, methods=['GET']):
    """
    Thêm một Api Object
    :param path:
    :param handler:
    :param endpoint:
    :param methods:
    :return:
    """
    get_app().add_url_rule(get_app().app_config.get_route_path(path), endpoint, handler, methods)
