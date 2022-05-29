from flask import Flask  #importing flask elements to make everything work
from flask import render_template
from flask import send_from_directory
import quicky.config
import quicky.logs
import pathlib
from flask_restful import Resource, Api
app_config = quicky.config.Config(__file__)
app = Flask(
    __name__,
    static_folder= app_config.full_static_dir,
    static_url_path=app_config.static_url,
    template_folder= app_config.full_template_path
)
api = Api(app)