"""
API liệt kê danh sách các file
"""
import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request
import api_models.documents as docs
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema


@fasty.api_post("/{app_name}/apps/register")
async def register_new_app(app_name: str, request: Request):
    """
    Tạo một application mới\n
    Mỗi một application là một isolate tenant bao gồm:\n
        1- Elastich search engine
        2- Mongo Database
        3- Seperated file partition

    :param app_name:
    :return:
    """
    return dict(
        error=dict(
            code="NotImplemenet",
            message="Chua code"
        )
    )
