"""
The pakage support for FastAPI
"""
import pathlib
import ReCompact.db_async
import os
path_to_yam_db =os.path.join(str(pathlib.Path(__file__).parent.parent.absolute()),"database.yaml")
print(path_to_yam_db)

ReCompact.db_async.load_config(path_to_yam_db)

from fastapi import FastAPI
import sys
app = None
def install_fastapi_app(module_name:str):
    global app
    app = FastAPI()
    setattr(sys.modules[module_name],"app",app)
    return app

def api_get(url_path:str):
    global app
    fn=app.get(url_path)
    return  fn

def api_post(url_path:str):
    global app
    fn=app.post(url_path)
    return  fn

