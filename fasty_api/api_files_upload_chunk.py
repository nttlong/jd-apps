import datetime
import os.path
import ReCompact_Kafka.producer
from fastapi import  File, Form,Response,Depends
from pydantic import BaseModel, Field
from typing import Union
import fasty
from .models import Error as ret_error
from ReCompact.db_async import get_db_context, ErrorType as db_error_type,sync as run_sync
import fasty.JWT
import api_models.documents as docs
import ReCompact.db_context
import ReCompact.dbm.DbObjects
import humanize
import threading
from api_models.Models_Kafka_Tracking import Sys_Kafka_Track
Sys_Kafka_Track_Doc= Sys_Kafka_Track()
class UploadChunkResult(BaseModel):
    SizeInHumanReadable: Union[str, None] = Field(description="Dung lương format dưới dạng text")
    SizeUploadedInHumanReadable: Union[str, None] = Field(description="Dung lương đã upload format dưới dạng text")
    Percent: Union[float, None] = Field(description="Phần trăm hoàn tất")
    NumOfChunksCompleted:Union[int,None]


class UploadFilesChunkInfoResult(BaseModel):
    Data: Union[UploadChunkResult, None] = Field(description="Kết quả nếu không lỗi")
    Error: Union[ret_error, None] = Field(description="Lỗi")


def __kafka_producer_delivery_report__(error, msg):
        """
        Hàm này dùng để tiếp nhận lỗi từ Kafka
        :param error:
        :param msg:
        :return:
        """
        import asyncio
        import json
        data =json.loads(msg.value().decode("utf8"))
        app_name =data["AppName"]
        topic_key =msg.topic()
        db_context = get_db_context(app_name)
        ret = db_context.insert_one(
            Sys_Kafka_Track_Doc,
            Sys_Kafka_Track_Doc.Data == data,
            Sys_Kafka_Track_Doc.Error == error,
            Sys_Kafka_Track_Doc.Topic == topic_key,
            Sys_Kafka_Track_Doc.CreatedOn == datetime.datetime.now()
        )


        if error:
            fasty.config.logger.debug("------------------------------------")
            fasty.config.logger.debug("Kafka server error")
            fasty.config.logger.debug(error)
            fasty.config.logger.debug(msg)
            fasty.config.logger.debug("------------------------------------")
        else:
            fasty.config.logger.info("------------------------------------")
            fasty.config.logger.info("Kafka server recive new topic")
            fasty.config.logger.debug(error)
            fasty.config.logger.debug(msg)
            fasty.config.logger.debug("------------------------------------")

@fasty.api_post("/{app_name}/files/upload", response_model=UploadFilesChunkInfoResult)
async def files_upload(app_name: str, FilePart: bytes = File(...),
                       UploadId: Union[str, None] = Form(...),
                       Index: Union[int, None] = Form(...),
                        token: str = Depends(fasty.JWT.oauth2_scheme)
                       ):
    topic_key = "files.services.upload"
    """
    topic báo hiệu 1 file đã được upload 
    """

    path_to_broker_share=None
    """
    Đường dẫn đến file share. 
    Một số xử lý thông qua Kafka đòi hỏi phải có file đính kèm
    và file này có thể có kích thước rất lớn lên đến vài chục GB.\n
    Các tiến trình trong Consumer có thể cần tham khảo đến nội dung file.
    Ví dụ một tiến trình trong Kafka Consumer xử lý 1 file Video có dung lượng 4GB
    Tiến trình sẽ đọc file này theo đường dẫn trong biến  path_to_broker_share
    path_to_broker_share: có thể là share file trong mang LAN, nếu tiến trình xử lý không cùng nằm trên 1 PC
    
    """

    ret = UploadFilesChunkInfoResult()
    db_name = await fasty.JWT.get_db_name_async(app_name)


    if db_name is None:
        return Response(status_code=403)
    if fasty.config.broker.enable:
        """
        Nếu có sử dụng broker
        """
        path_to_broker_share = os.path.join(fasty.config.broker.share_directory, db_name)
        if not os.path.isdir(path_to_broker_share):
            """
            Nếu không có thư mục tạo luôn
            """
            os.makedirs(path_to_broker_share)



    db_context = get_db_context(app_name)
    gfs = db_context.get_grid_fs()
    upload_item = await db_context.find_one_async(docs.Files,docs.Files._id==UploadId)
    if upload_item is None:
        ret.Error=ret_error()
        ret.Error.Code=db_error_type.DATA_NOT_FOUND
        ret.Error.Fields=['UploadId']
        ret.Error.Message =f"Upload with '{UploadId}' was not found"
        return ret
    if fasty.config.broker.enable:
        path_to_broker_share = os.path.join(path_to_broker_share,f"{UploadId}.{upload_item.get(docs.Files.FileExt.__name__)}")
    file_size=upload_item[docs.Files.SizeInBytes.__name__]
    size_uploaded=upload_item.get(docs.Files.SizeUploaded.__name__,0)
    num_of_chunks_complete = upload_item.get(docs.Files.NumOfChunksCompleted.__name__,0)
    nun_of_chunks = upload_item.get(docs.Files.NumOfChunks.__name__,0)
    main_file_id= upload_item.get(docs.Files.MainFileId.__name__,None)
    chunk_size_in_bytes = upload_item.get(docs.Files.ChunkSizeInBytes.__name__,0)
    server_file_name =upload_item.get(docs.Files.ServerFileName.__name__)

    if num_of_chunks_complete==0:
        fs =ReCompact.db_context.mongodb_file_create(
            db_context.db.delegate,
            server_file_name,
            chunk_size_in_bytes,
            file_size=file_size
        )
        ReCompact.db_context.mongodb_file_add_chunks(db_context.db.delegate,fs._id,Index,FilePart)
        if fasty.config.broker.enable:
            if not os.path.isfile(path_to_broker_share):
                with open(path_to_broker_share, "wb") as file:
                    file.write(FilePart)
            else:
                with open(path_to_broker_share, "ab") as file:
                    file.write(FilePart)

        main_file_id=fs._id
    else:
        ReCompact.db_context.mongodb_file_add_chunks(db_context.db.delegate,main_file_id,Index, FilePart)
        if fasty.config.broker.enable:
            if not os.path.isfile(path_to_broker_share):
                with open(path_to_broker_share, "wb") as file:
                    file.write(FilePart)
            else:
                with open(path_to_broker_share, "ab") as file:
                    file.write(FilePart)
    size_uploaded +=len(FilePart)
    ret.Data=UploadChunkResult()
    ret.Data.Percent=round((size_uploaded*100)/file_size,2)
    ret.Data.SizeUploadedInHumanReadable= humanize.filesize.naturalsize(size_uploaded)
    num_of_chunks_complete+=1
    ret.Data.NumOfChunksCompleted=num_of_chunks_complete
    ret.Data.SizeInHumanReadable= humanize.filesize.naturalsize(file_size)
    status=0
    if num_of_chunks_complete==nun_of_chunks:
        status=1
        if fasty.config.broker.enable:
            def send():
                upload_item["UploadID"] = upload_item["_id"]
                try:
                    ReCompact_Kafka.producer.Bootstrap(
                        fasty.config.broker.servers,
                        delivery_report=__kafka_producer_delivery_report__
                    ).send_msg_sync(topic_key, dict(
                        AppName=app_name,
                        FilePath=path_to_broker_share,
                        UploadInfo=upload_item

                    ))
                except Exception as e:
                    fasty.config.logger.debug(e)
            th=  threading.Thread(target=send,args=())
            th.start()
            th.join()
            """
            Để bảo đảm tốc độ việc gời 1 thông điệp đến Kafka cần phải thông qua 1 tiến trình
            """

    await db_context.update_one_async(
        docs.Files,
        docs.Files._id==UploadId,
        docs.Files.SizeUploaded==size_uploaded,
        docs.Files.NumOfChunksCompleted==num_of_chunks_complete,
        docs.Files.Status==status,
        docs.Files.MainFileId==main_file_id

    )
    return ret
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
