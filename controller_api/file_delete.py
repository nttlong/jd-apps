import datetime

from flask import request, Response
from flask_restful import Resource
import db_connection
import quicky.object_contraints
import humanize
import api_models.Model_Files
import quicky
import uuid
import mimetypes
import os
cnn = db_connection.connection
class FileDelete(Resource):
    def post(self,app_name):
        data = request.get_json(force=True)
        if data.get("UploadId",None) is None:
            err= quicky.object_contraints.Error()
            err.field="UploadId"
            err.message="UploadId is require"
            err.code=quicky.object_contraints.ErrorCode.REQUIRE
            return dict(
                error=err
            )
        files = api_models.Model_Files.DocUploadRegister(cnn,app_name)
        files.delete_one(
            files._id==data["UploadId"]
        )
        return data

quicky.api_add_resource(FileDelete, "/files/<app_name>/delete")