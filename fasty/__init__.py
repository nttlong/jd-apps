"""
The pakage support for FastAPI
"""
import mimetypes
mimetypes.types_map[".js"]="application/javascript"
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import traceback
import pathlib
import ReCompact.db_async
from fastapi import logger
import os
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
path_to_yam_db =os.path.join(str(pathlib.Path(__file__).parent.parent.absolute()),"database.yaml")
print(path_to_yam_db)

ReCompact.db_async.load_config(path_to_yam_db)
from . import start
from fastapi import FastAPI
import ReCompact.db_async
import sys
app = None
config:start.Config
def load_config(app_path,app_name):
    global config

    config = start.Config(app_path,app_name)
    ReCompact.db_async.set_connection_string(config.db.connection_string())
def install_fastapi_app(module_name:str):
    global app
    global config
    app = FastAPI()
    app.middleware('http')(catch_exceptions_middleware)
    setattr(sys.modules[module_name],"app",app)
    app.mount("/static", StaticFiles(directory=config.app.static), name="static")
    return app

def page_get(url_path:str,response_class=HTMLResponse):
    global app
    fn = app.get(url_path, response_class=response_class)
    return fn


def api_get(url_path:str,response_class=None):
    global app
    if config.app.api is not None and config.app.api!="":
        if response_class is None:
            fn = app.get(config.app.api + url_path)
            return fn
        else:
            fn = app.get(config.app.api+url_path,response_class=response_class)
            return fn
    else:
        if response_class is None:
            fn = app.get(url_path)
            return fn
        else:
            fn=app.get(url_path,response_class=response_class)
            return  fn

def api_post(url_path:str,response_class=None,response_model=None):
    global app
    if config.app.api is not None and config.app.api != "":
        if response_class is None:
            if response_model is None:
                fn = app.post(config.app.api+url_path)
                return fn
            else:
                fn = app.post(config.app.api + url_path,response_model=response_model)
                return fn
        else:
            fn = app.post(config.app.api + url_path,response_class=response_class)
            return fn
    else:
        if response_class is None:
            fn = app.post(url_path)
            return fn
        else:
            fn=app.post(url_path,response_class=response_class)
            return  fn
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        import fasty.start
        fasty.start.__logger__.debug(e)
        fasty.start.__logger__.debug(traceback.format_exc())
        # you probably want some kind of logging here
        return Response("Internal server error", status_code=500)


