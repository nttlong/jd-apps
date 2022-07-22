"""
API liệt kê danh sách các file
"""
import datetime
import re
from time import strftime
from time import gmtime
import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request,Response
from pydantic import BaseModel
import api_models.documents as docs
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status

import services.accounts
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema
import humanize.time
import fasty.JWT
from pathlib import Path
from fasty.context import Context, AccessExpireEnum
from . import api_files_content
from services.accounts import AccountService, AccountRepository
from services.files import FilesService
from kink import inject
@fasty.api_post("/{app_name}/files")
async def get_list_of_files(
        app_name: str,
        filter: api_files_schema.Filter,
        request: Request,token: str = Depends(fasty.JWT.oauth2_scheme),
        context: Context = Depends(Context())
        ):
    """
    APi này sẽ liệt kê danh sách các file
    :param app_name:
    :return:
    """

    share_key = await context.create_share_key(
        'cross',
        AccessExpireEnum.PRIVATE,
        api_files_content.get_content_of_files_v2)
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
        docs.Files.OCRFileId,
        docs.Files.PdfFileId,
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

    )
    if filter.ValueSearch and filter.ValueSearch !="":
        agg.match(
            docs.Files.FileName==re.compile(filter.ValueSearch)
        )

    agg.sort(
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
                docs.Files._id==x["UploadId"],
                docs.Files.FileNameOnly==file_name_only
                )
            x[docs.Files.FileNameOnly.__name__] =file_name_only
        if x.get(docs.Files.RegisterOnDays.__name__,None) is None:
            date_val = x.get(docs.Files.RegisterOn.__name__,None)
            if date_val is not None and isinstance(date_val,datetime.datetime):
                await  db.update_one_async(
                    docs.Files,
                    docs.Files._id==x["UploadId"],
                    docs.Files.RegisterOnDays == date_val.day,
                    docs.Files.RegisterOnMonths ==date_val.month,
                    docs.Files.RegisterOnYears == date_val.year,
                    docs.Files.RegisterOnHours == date_val.hour,
                    docs.Files.RegisterOnMinutes == date_val.minute,
                    docs.Files.RegisterOnSeconds==date_val.second
                )
        full_filename_without_extenstion =x.get(docs.Files.FullFileNameWithoutExtenstion.__name__)
        if x.get(docs.Files.FullFileNameWithoutExtenstion.__name__) is None:
            full_filename =x.get(docs.Files.FullFileName.__name__)
            full_dir_path = str(Path(full_filename).parent)
            filename_only = Path(full_filename).stem
            full_filename_without_extenstion = f"{full_dir_path}/{filename_only}"
            await  db.update_one_async(
                docs.Files,
                docs.Files._id == x["UploadId"],
                docs.Files.FullFileNameWithoutExtenstion ==full_filename_without_extenstion,
                docs.Files.FullFileNameWithoutExtenstionLower == full_filename_without_extenstion.lower(),
            )
        if x.get(docs.Files.FullFileNameLower.__name__) is None:
            full_filename =x.get(docs.Files.FullFileName.__name__)

            await  db.update_one_async(
                docs.Files,
                docs.Files._id == x["UploadId"],
                docs.Files.FullFileNameLower ==full_filename.lower()
            )
        x["UrlOfServerPath"] = url+f"/{app_name}/file/{x[docs.Files.FullFileName.__name__]}?{share_key.key}={share_key.value}"
        x["AppName"]=app_name
        x["RelUrlOfServerPath"] = f"/{app_name}/file/{x[docs.Files.FullFileName.__name__]}"
        x["ThumbUrl"]= url+f"/{app_name}/thumb/{x['UploadId']}/{x[docs.Files.FileName.__name__]}.png"
        if x.get("Media") and x["Media"].get("Duration"):
            x["DurationHumanReadable"]=strftime("%H:%M:%S", gmtime(x["Media"]["Duration"]))
        if x.get(docs.Files.OCRFileId.__name__):
            """
            /{app_name}/file-ocr/{directory:path}
            """
            x[docs.Files.OCRFileId.__name__]=None
            x["OcrContentUrl"] = url + f"/{app_name}/file-ocr/{full_filename_without_extenstion}.pdf"
        if x.get(docs.Files.PdfFileId.__name__):
            x.get(docs.Files.PdfFileId.__name__)
            x["PdfContentUrl"] = url + f"/{app_name}/file-pdf/{full_filename_without_extenstion}.pdf"





    return ret_list

