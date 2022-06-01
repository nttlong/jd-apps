from flask_restful import Resource
import flask_restful
import api_models.Model_Files
import fwebapi.database
import api_models.ModelApps

cnn = fwebapi.database.connection

class Apps(Resource):
    def post(self, app_name):
        if app_name != "admin":
            return []
        apps = api_models.ModelApps.sys_applications(cnn,fwebapi.database.db_config["authSource"])
        apps.sort(
            apps.RegisteredOn.desc(),
            apps.Name.asc()
        )
        return list(apps)