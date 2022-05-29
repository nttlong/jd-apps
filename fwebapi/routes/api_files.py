from . import app
from . import api
from . import app_config
from . import Resource
import api_models.Model_Files
import pymongo.mongo_client
cnn = pymongo.mongo_client.MongoClient(
    host="localhost",
    port=27017,
    username="yes",
    password="123456",
    authSource="xxx",



)
db=cnn.get_database("XXXX")
model =api_models.Model_Files.DocUploadRegister
files = api_models.Model_Files.DocUploadRegister()
files<<db
files.update_one(model._id.f=="123", {})



class Quotes(Resource):
    def get(self,app_name):
        print(files)
        fx=files.ServerFileName
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