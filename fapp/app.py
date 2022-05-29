from flask import Flask  #importing flask elements to make everything work
from flask import render_template
from flask import send_from_directory
import quicky.config
import quicky.logs
import pathlib
app_config = quicky.config.Config(__file__)
app = Flask(
    __name__,
    static_folder= app_config.full_static_dir,
    static_url_path=app_config.static_url,
    template_folder= app_config.full_template_path
)



@app.route(app_config.get_route_path('/<path:path>'))
def single_page_app(path):
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)

@app.route(app_config.get_route_path('/'))
@app.route('/index')
def index():
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)
if __name__ == '__main__':
    app_config.logger.info("------------------------------------------------------")
    app_config.logger.info("web start with:")
    app_config.logger.info(dict(debug=app_config.debug, host=app_config.host, port=app_config.port))
    app_config.logger.info("------------------------------------------------------")
    app.run(
          debug=app_config.debug,
          host= app_config.host,
          port=app_config.port
    )



