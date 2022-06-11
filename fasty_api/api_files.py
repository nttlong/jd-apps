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


@fasty.api_post("/{app_name}/files/")
async def get_list_of_files(app_name: str, filter: api_files_schema.Filter, request: Request):
    """
    APi này sẽ liệt kê danh sách các file
    :param app_name:
    :return:
    """
    db = db_async.get_db_context(app_name)
    agg = db.aggregate(docs.Files)
    agg.project(
        # docs.Files._id,
        docs.Files.FileName,
        docs.Files.FullFileName,
        docs.Files.HasThumb,
        docs.Files.ServerFileName,
        docs.Files.SizeInHumanReadable,
        docs.Files.Status,
        docs.Files.MimeType,
        # docs.Files.MainFileId,
        FileSize=docs.Files.SizeInBytes,
        ModifiedOn=docs.Files.LastModifiedOn,
        UploadId=docs.Files._id,
        CreatedOn=docs.Files.RegisterOn
    ).sort(
        ReCompact.dbm.FIELDS.ModifiedOn.desc(),
        ReCompact.dbm.FIELDS.CreatedOn.desc(),
        ReCompact.dbm.FIELDS.FileSize.desc()

    ).pager(
        filter.PageIndex, filter.PageSize
    )

    ret_list = await agg.to_list_async()
    url = f"{request.url.scheme}://{request.url.hostname}"
    if request.url.port not in [80, 443]:
        url += f":{request.url.port}"
    for x in ret_list:
        x["UrlOfServerPath"] = url+f"/files/{app_name}/directory/{x['UploadId']}/{x['FileName']}"

    return ret_list

