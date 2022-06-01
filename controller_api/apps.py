from flask_restful import Resource, Api

from flask_restful import Resource
import flask_restful
import api_models.Model_Files
import pymongo.mongo_client
import asyncio
import quicky
import datetime

import api_models.ModelApps
import db_connection
cnn = db_connection.connection
default_db_name =db_connection.default_db_name
from flask import Flask, jsonify, request
class Apps(Resource):
    def post(self, app_name):
        if app_name != "admin":
            return []
        apps = api_models.ModelApps.sys_applications(cnn,default_db_name)
        apps.sort(
            apps.RegisteredOn.desc(),
            apps.Name.asc()
        )
        return list(apps)

class App(Resource):
    def post(self, app_name):
        json_data = request.get_json(force=True)
        find_app_name = json_data.get("AppName",None)

        if app_name != "admin":
            return []
        apps = api_models.ModelApps.sys_applications(cnn,default_db_name)
        ret =apps.find_one(apps.Name==find_app_name)
        return ret
quicky.api_add_resource(Apps, '/apps/<app_name>/list')
quicky.api_add_resource(App, '/apps/<app_name>/get')


