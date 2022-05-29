from flask import Flask  #importing flask elements to make everything work

import quicky.config
import quicky.logs
import pathlib
app_config = quicky.config.Config(pathlib.Path(__file__).parent.parent)
app = Flask(
    __name__,
    static_folder= app_config.full_static_dir,
    static_url_path=app_config.static_url,
    template_folder= app_config.full_template_path
)
