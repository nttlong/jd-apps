"""
API liệt kê danh sách các file
"""
import datetime

import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request,Response
from pydantic import BaseModel
import api_models.documents as docs
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema
import fasty.JWT
from pathlib import Path
@fasty.api_post("/{app_name}/files")
async def get_list_of_files(app_name: str, filter: api_files_schema.Filter, request: Request,token: str = Depends(fasty.JWT.oauth2_scheme)):
    """
    APi này sẽ liệt kê danh sách các file
    :param app_name:
    :return:
    """
    db_name = await fasty.JWT.get_db_name_async(app_name)
    if db_name is None:
        return Response(status_code=403)
    db = db_async.get_db_context(db_name)
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
        docs.Files.IsPublic,
        docs.Files.HasThumb,
        # docs.Files.MainFileId,
        FileSize=docs.Files.SizeInBytes,
        ModifiedOn=docs.Files.LastModifiedOn,
        UploadId=docs.Files._id,
        CreatedOn=docs.Files.RegisterOn,
        Media=dict(
            Height=docs.Files.VideoResolutionHeight,
            Width = docs.Files.VideoResolutionWidth,
            Duration =docs.Files.VideoDuration,
            FPS = docs.Files.VideoFPS
        )

    ).sort(
        ReCompact.dbm.FIELDS.ModifiedOn.desc(),
        ReCompact.dbm.FIELDS.CreatedOn.desc(),
        ReCompact.dbm.FIELDS.FileSize.desc()

    ).pager(
        filter.PageIndex, filter.PageSize
    )

    ret_list = await agg.to_list_async()
    url = fasty.config.app.api_url

    for x in ret_list:
        if x.get(docs.Files.FileNameOnly.__name__,None) is None:
            file_name_only =Path(x[docs.Files.FileName.__name__]).stem
            await  db.update_one_async(
                docs.Files,
                docs.Files.ServerFileName==x[docs.Files.ServerFileName.__name__],
                docs.Files.FileNameOnly==file_name_only
                )
            x[docs.Files.FileName.__name__] =file_name_only
        if x.get(docs.Files.RegisterOnDays.__name__,None) is None:
            date_val = x.get(docs.Files.RegisterOn.__name__,None)
            if date_val is not None and isinstance(date_val,datetime.datetime):
                await  db.update_one_async(
                    docs.Files,
                    docs.Files.ServerFileName==x[docs.Files.ServerFileName.__name__],
                    docs.Files.RegisterOnDays == date_val.day,
                    docs.Files.RegisterOnMonths ==date_val.month,
                    docs.Files.RegisterOnYears == date_val.year,
                    docs.Files.RegisterOnHours == date_val.hour,
                    docs.Files.RegisterOnMinutes == date_val.minute,
                    docs.Files.RegisterOnSeconds==date_val.second
                )

        x["UrlOfServerPath"] = url+f"/{app_name}/file/{x['UploadId']}/{x['FileName']}"
        x["AppName"]=app_name
        x["RelUrlOfServerPath"] = f"/{app_name}/file/{x['UploadId']}/{x['FileName']}"
        x["ThumbUrl"]= url+f"/{app_name}/thumb/{x['UploadId']}/{x[docs.Files.FileName.__name__]}.png"


    return ret_list

