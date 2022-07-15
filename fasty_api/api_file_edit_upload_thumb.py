import datetime
import os.path

import bson
from fasty.context import Context
import ReCompact_Kafka.producer
from fastapi import File, Form, Response, Depends
from pydantic import BaseModel, Field
from typing import Union
import fasty
from fasty import config
from .models import Error as ret_error
from ReCompact.db_async import get_db_context, ErrorType as db_error_type, sync as run_sync
import fasty.JWT
import api_models.documents as docs
import ReCompact.db_context
import ReCompact.dbm.DbObjects
import humanize
import threading


class UploadUpdateThumInfo(BaseModel):
    """
    Return information of this api if successfull call
    """
    pass


class UploadUpdateThumbResult(BaseModel):
    """
    -----------------------------------------------------------------------------------------
    Mô tà kết quả trả về sau khi cập nhật
    -----------------------------------------------------------------------------------------
    """
    Data: Union[UploadUpdateThumInfo, None]
    Error: Union[ret_error, None]


# class UploadUpdateThumbResult(BaseModel):
#     SizeInHumanReadable: Union[str, None] = Field(description="Dung lương format dưới dạng text")
#     SizeUploadedInHumanReadable: Union[str, None] = Field(description="Dung lương đã upload format dưới dạng text")
#     Percent: Union[float, None] = Field(description="Phần trăm hoàn tất")
#     NumOfChunksCompleted: Union[int, None]


@fasty.api_post("/{app_name}/file/modify/thumb", response_model=UploadUpdateThumbResult)
async def files_update_thumb(app_name: str, ThumbFile: bytes = File(...),
                       UploadId: Union[str, None] = Form(...),
                       token: str = Depends(fasty.JWT.oauth2_scheme),
                       context: Context =Depends(Context())):
    """
    As usually, every uploaded content has its own a thumbnail. <br/>
    Thee could replace that thumbnail by call this api</br>
    :param app_name: The application's name <br/>
    :param ThumbFile: File Thumb to upload <br/>
    :param UploadId:
    :param token:
    :return:
    """
    if context.is_forbidden: return context.get_forbidden_response()
    if context.access_application_name!= context.application_name:
        return Response(status_code=403)
    fx= context
    pass
