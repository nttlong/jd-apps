from . import app
from . import api
from . import app_config
from . import Resource
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