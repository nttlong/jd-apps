import os

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
from flask import request
import api_models.ModelApps
import re
import json
from flask import Response,stream_with_context
import mimetypes
cnn = fwebapi.database.connection

from flask import Flask, jsonify, request
cnn = fwebapi.database.connection

from flask import Flask, jsonify, request
class UploadServices(Resource):
    def post(self, app_name):
        data = request.get_json(True)
        if data.get("FileName",None) is None:
            return dict(
                error=dict(
                    message="FileName was not found"
                )
            )

        return dict(
                error=dict(
                    message="FileName was not found"
                )
            )
api.add_resource(UploadServices, app_config.get_route_path("/files/<app_name>/upload/register"))

