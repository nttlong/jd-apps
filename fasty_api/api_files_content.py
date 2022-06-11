"""
API liệt kê danh sách các file
"""
import motor

import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request, Header, Response
import api_models.documents as docs
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema
from api_models.documents import Files
from ReCompact import db_async
from fastapi.responses import StreamingResponse
import os
import mimetypes
import fasty.mongo_fs_http_streaming

@fasty.api_get("/{app_name}/file/{directory:path}")
async def get_content_of_files(app_name: str, directory: str, request: Request):
    """
    Xem hoặc tải nội dung file
    :param app_name:
    :return:
    """
    CHUNK_SIZE = 1024 * 1024
    cntx = db_async.get_db_context(app_name)
    file_info = await cntx.find_one_async(Files, Files.FullFileName == directory.lower())
    if file_info:
        fs_id = file_info[Files.MainFileId.__name__]
    fsg = await cntx.get_file_by_id(file_info[Files.MainFileId.__name__])
    content_type, _ = mimetypes.guess_type(directory)
    res= await fasty.mongo_fs_http_streaming.streaming(fsg,request,content_type)
    fsg.close()
    return res
