import datetime

from flask import Flask  #importing flask elements to make everything work
from flask import render_template
from flask import send_from_directory
import quicky.config
import quicky.logs
import pathlib
from flask_restful import Resource, Api
from flask_cors import CORS
import pathlib


app_config = quicky.config.Config(str(pathlib.Path(__file__).parent.parent))
from flask import json
class ModelEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return super(ModelEncoder, self).default(o)

app = Flask(
    __name__,
    static_folder= app_config.full_static_dir,
    static_url_path=app_config.static_url,
    template_folder= app_config.full_template_path
)
app.json_encoder = ModelEncoder
CORS(app)
@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response
api = Api(app)
