"""
API liệt kê danh sách các file
"""
import fasty
import api_models.documents as docs
from ReCompact import db_async
import json
from db_connection import connection,default_db_name
@fasty.api_post("/files/{app_name}/list")
async def get_list_of_files(app_name:str):
    """
    APi này sẽ liệt kê danh sách các file
    :param app_name:
    :return:
    """
    db = db_async.get_db_context(app_name)

    ret = await db.find_async(docs.Files, {},2)
    return ret
