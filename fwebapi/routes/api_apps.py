from . import app
from . import api
from . import app_config
from flask_restful import Resource
import flask_restful
import api_models.Model_Files
import pymongo.mongo_client
import asyncio
import quicky
import datetime
import fwebapi.database
import api_models.ModelApps

cnn = fwebapi.database.connection

class Apps(Resource):
    def post(self, app_name):
        if app_name != "admin":
            return []
        db = cnn.get_database(fwebapi.database.db_config["authSource"])
        apps = api_models.ModelApps.sys_applications()
        apps << db




        return list(apps)



api.add_resource(Apps, app_config.get_route_path('/apps/<app_name>/list'))
