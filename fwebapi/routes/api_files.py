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
import api_models.ModelApps
import re

from flask import Response,stream_with_context
import mimetypes
cnn = fwebapi.database.connection

from flask import Flask, jsonify, request
class Files(Resource):
    def post(self, app_name):
        #http://192.168.18.36:5011/api/files/app-test-dev/directory/2c071ba4-eea9-499e-8481-db580882a183/one%20of%20us.mp4
        json_data = request.get_json(force=True)
        page_index = json_data.get("PageIndex", 0)
        page_size = json_data.get("PageSize", 20)
        field_search= json_data.get("FieldSearch",None)
        value_search = json_data.get("ValueSearch",None)
        files = api_models.Model_Files.DocUploadRegister(cnn,app_name)
        if field_search is not None and value_search is not None:
            files.filter(
                getattr(files,field_search)== re.compile(value_search)
            )
        files.skip(page_index*page_size)
        files.limit(page_size)
        ret =list(files)
        for x in ret:
            x["UrlOfServerPath"]=f"{app_config.full_url_app}/{self.endpoint}/{app_name}/directory/{x['FullFileName']}"

        return ret





api.add_resource(Files, app_config.get_route_path('/files/<app_name>/list'))
# @BluePrintStream.core.route(app_config.get_route_path('/files/<app_name>/<path:directory>'))
@app.route(app_config.get_route_path('/files/<app_name>/<path:directory>'), methods=["GET"])
def source(app_name,directory):
    import ReCompact.db_context
    files = api_models.Model_Files.DocUploadRegister(cnn, app_name)
    if directory.startswith("directory/"):
        directory = directory["directoty".__len__() + 1:]
    file_item = files.find_one(files.FullFileName == directory.lower())
    if file_item is None:
        return Response(status=404)
    fs = None
    if file_item.get("MainFileId", None) is not None:
        fs = ReCompact.db_context.get_mongodb_file_by_file_id(
            file_id=file_item["MainFileId"],
            db=cnn.get_database(app_name)

        )
    else:
        fs = ReCompact.db_context.get_mongodb_file_by_file_name(
            file_name=file_item["ServerFileName"],
            db=cnn.get_database(app_name)

        )
        files.update_one(
            files.ServerFileName == file_item["ServerFileName"],
            files.set(
                files.MainFileId == fs._id
            )
        )
    if fs is None:
        return Response(status=404)
    else:
        mime_type, _ = mimetypes.guess_type(directory)
        import flask_streaming.grid_fs_stream
        return flask_streaming.grid_fs_stream.streaming_content(
            mime_type=mime_type,
            request=request,
            fs=fs,
            streaming_segment_size_in_KB= app_config.media.streaming_segment_size_in_KB,
            streaming_buffering_in_KB= app_config.media.streaming_buffering_in_KB

        )

