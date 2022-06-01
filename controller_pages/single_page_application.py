import quicky
from flask import render_template
import quicky
app =quicky.get_app()
@app.route(app.app_config.get_route_path('/<path:path>'))
def single_page_app(path):

    return render_template('index.html',app=app.app_config)

@app.route(app.app_config.get_route_path('/'))
def index():

    return render_template('index.html',app=app.app_config)