from flask import request,Response
from flask_restful import Resource
import quicky
import db_connection
cnn = db_connection.connection

class FileRegister(Resource):
    def post(self,app_name):
        print(app_name)
        return app_name
    def get(self,app_name):
        print(app_name)
        return app_name

quicky.api_add_resource(FileRegister,"/files/<app_name>/upload/register")