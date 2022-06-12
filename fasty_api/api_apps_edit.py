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


@fasty.api_post("/{app_name}/apps/edit")
async def application_edit(app_name: str, request: Request):
    """
    Cập nhật lại thông tin applcation

    :param app_name:
    :return:
    """
    return dict(
        error=dict(
            code="NotImplemenet",
            message="Chua code"
        )
    )
