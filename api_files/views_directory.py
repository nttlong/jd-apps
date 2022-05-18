from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import ReCompact.db_context
import ReCompact.dbm
import api_models.Model_Files
import ReCompact.HttpStream
@require_http_methods(["GET"])
def source(request,app_name,full_path):
    db = ReCompact.db_context.get_db(app_name)
    upload_item = ReCompact.dbm.DbObjects.find_one_to_dict(
        db,
        api_models.Model_Files.DocUploadRegister,
        ReCompact.dbm.FILTER.FullFileName == full_path

    )
    server_file_name = upload_item["ServerFileName"]
    fs = ReCompact.db_context.get_mongodb_file_by_file_name(db,server_file_name)
    ReCompact.HttpStream.streaming_mongo_db_fs(request,fs)

    return  ReCompact.HttpStream.streaming_mongo_db_fs(request,fs)