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

class Quotes(Resource):
    def get(self,app_name):
        return {
            'William Shakespeare': {
                'quote': ['Love all,trust a few,do wrong to none',
                'Some are born great, some achieve greatness, and some greatness thrust upon them.']
        },
        'Linus': {
            'quote': ['Talk is cheap. Show me the code.']
            }
        }

api.add_resource(Quotes, app_config.get_route_path('/<app_name>'))

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



