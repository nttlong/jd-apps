import flask
from flask_restful import Resource, Api
from . import config
__app__= None
__api_dir__= '/api'

class QuickyApp(flask.app.Flask):
    def __init__(self,name,app_config:config.Config):
        super().__init__(
            name,
            static_folder=app_config.full_static_dir,
            static_url_path=app_config.static_url,
            template_folder=app_config.full_template_path
        )
        self.app_config=app_config
        self.api = Api(self)
        global __app__
        __app__= self
def set_api_die(path):
    global __api_dir__
    __api_dir__=path
def get_app()->QuickyApp:
    global __app__
    return __app__
def api_add_resource(controller_class,url_path:str):
    global __api_dir__
    if __api_dir__=='/':
        get_app().api.add_resource(controller_class,get_app().app_config.get_route_path(url_path))
    else:
        get_app().api.add_resource(controller_class,get_app().app_config.get_route_path(__api_dir__+ url_path))
def add_handler(path, handler,endpoint,methods=['GET']):
    get_app().add_url_rule(get_app().app_config.get_route_path(path),endpoint,handler,methods)