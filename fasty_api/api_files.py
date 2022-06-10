"""
API liệt kê danh sách các file
"""
import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request,Response
import api_models.documents as docs
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema


@fasty.api_post("/apps/{app_name}/list")
async def get_list_of_files(app_name: str, filter: api_files_schema.Filter, request: Request):
    """
    Get list of application which  has completely register before
    \n
    :param app_name: \n If thy does not use 'admin', the API server will refuse \n
    :return: [\n {\n
        AppId:".." Id of Application, \n
        Name:"" Application name \n
        Decription:"..." Decription of app \n
    },..\n]
    """

    if app_name!='admin':
        return Response(status_code=403)
    db = db_async.get_db_context(app_name)
    agg = db.aggregate(docs.Apps)
    agg.project(
        # docs.Files._id,

        docs.Apps.Name,
        docs.Apps.Domain,
        docs.Apps.LoginUrl,
        docs.Apps.ReturnUrlAfterSignIn,
        docs.Apps.Decription,
        CreatedOn= docs.Apps.RegisteredOn,
        AppId=docs.Apps._id
    ).sort(
        ReCompact.dbm.FIELDS.CreatedOn.desc(),
        ReCompact.dbm.FIELDS.Name.desc()

    ).pager(
        filter.PageIndex, filter.PageSize
    )

    ret_list = await agg.to_list_async()
    return ret_list
