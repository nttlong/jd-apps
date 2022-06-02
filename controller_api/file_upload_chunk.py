import datetime

from flask import request, Response
from flask_restful import Resource
import db_connection
import quicky.object_contraints
import humanize
import api_models.Model_Files
import quicky
import uuid
import mimetypes
import os
import json
import controller_api.file_upload
import werkzeug.datastructures
import ReCompact.db_context
cnn = db_connection.connection
app_config = quicky.get_app().app_config


"""
Cấu hình app đang chạy
"""
@quicky.object_contraints.contraints()
class FileUploadChunkInfo:
    UploadId=(str,True)
    """
    Thông tin của UploadId
    """
    Index=(int,True)
    """
    CHỉ mục của phân đoạn
    """
from controller_api.file_upload import FileProgressInfo


class FileUploadChunk(Resource):
    """
    Upload controller
    """

    def post(self, app_name):

        data = request.form.get('data', '{}')
        data=json.loads(data)
        upload_chunk_data = FileUploadChunkInfo(data)
        err = upload_chunk_data.get_error()
        if err:
            err.message = f"upload chunk require FilePart,UploadId,Index(index of chunk). FilePart is a chunk file in which was wrap in HTML File\n" \
                          f"By using var filePart=new File([blog of file par chunk],'any name thee would like\n" \
                          f"Then use var formData = new FormData()'\n" \
                          f"formData.append('FilePart', filePart )\n" \
                          f"Full example look like these:\n" \
                          f"var formData = new FormData()\n" \
                          f"var start=0;end=math.min(star+chunkSizeInBytes,fileUpload.size);\n" \
                          f"var filePartBlog = fileUpload.slice(start, end)\n" \
                          f"var filePart = new File([filePartBlog], fileUpload.name);\n" \
                          f"formData.append('FilePart', filePart);" \
                          f"var data={{UploadId:<UploadId>,Index:<index of chunk>}}\n" \
                          f"formData.append('data', JSON.stringify(checkData.data))\n" \
                          f"var fetcher = await fetch(url, {{\n" \
                          f"method: 'POST',\n" \
                          f"body: formData\n" \
                          f"}});"
            return dict(
                error=err.to_dict()
            )
        if request.files.get("FilePart",None) is None:
            err = quicky.object_contraints.Error()
            err.code = quicky.object_contraints.ErrorCode.REQUIRE
            err.field = "FilePart"
            err.message=f"upload chunk require FilePart. FilePart is a chunk file in which was wrap in HTML File\n" \
                        f"By using var filePart=new File([blog of file par chunk],'any name thee would like\n" \
                        f"Then use var formData = new FormData()'\n" \
                        f"formData.append('FilePart', filePart )\n" \
                        f"Full example look like these:\n" \
                        f"var formData = new FormData()\n" \
                        f"var start=0;end=math.min(star+chunkSizeInBytes,fileUpload.size);\n" \
                        f"var filePartBlog = fileUpload.slice(start, end)\n" \
                        f"var filePart = new File([filePartBlog], fileUpload.name);\n" \
                        f"formData.append('FilePart', filePart);" \
                        f"var data={{UploadId:<UploadId>,Index:<index of chunk>}}\n" \
                        f"formData.append('data', JSON.stringify(checkData.data))\n" \
                        f"var fetcher = await fetch(url, {{\n" \
                        f"method: 'POST',\n" \
                        f"body: formData\n" \
                        f"}});"
            return dict(
                error = err.to_dict()
            )
        file_part = request.files.get("FilePart")
        if not isinstance(file_part,werkzeug.datastructures.FileStorage):
            err = quicky.object_contraints.Error()
            err.code = quicky.object_contraints.ErrorCode.INVALID_DATA_TYPE
            err.field = "FilePart"
            return dict(
                error=err.to_dict()
            )

        files = api_models.Model_Files.DocUploadRegister(cnn,app_name)
        file_data = files.find_one(
            files._id==upload_chunk_data.UploadId
        )
        if file_data==None:
            err = quicky.object_contraints.Error()
            err.code = quicky.object_contraints.ErrorCode.ITEM_WAS_NOT_FOUND
            err.message=f"{upload_chunk_data.UploadId} was not found"
            err.field="UploadId"
            return dict(
                error=err.to_dict()
            )

        progess_info = controller_api.file_upload.FileProgressInfo(file_data)

        err = progess_info.get_error()
        if err:
            return dict(
                error= err.to_dict()
            )
        app_db = cnn.get_database(app_name)
        fs= None
        main_file_id =None
        progess_info.ChunkIndex=upload_chunk_data.Index

        if progess_info.ChunkIndex==0:
            fs = ReCompact.db_context.mongodb_file_create(
                db=app_db,
                file_name= progess_info.ServerFileName,
                chunk_size=progess_info.ChunkSizeInBytes,
                file_size= progess_info.FileSize
            )
            files.update_one(
                files._id== progess_info.UploadId,
                files.set(
                    files.MainFileId==fs._id
                )
            )
            main_file_id = fs._id
        else:
            upload_item = files.find_one(
                files._id== progess_info.UploadId
            )
            if not upload_item:
                err = quicky.object_contraints.Error()
                err.code= quicky.object_contraints.ErrorCode.ITEM_WAS_NOT_FOUND
                err.message=f"{progess_info.UploadId} was not found"
                return dict(error=err.to_dict() )
            if upload_item.get(files.MainFileId.__name__,None) is None:
                err = quicky.object_contraints.Error()
                err.code = quicky.object_contraints.ErrorCode.ITEM_WAS_NOT_FOUND
                err.message = f"{progess_info.UploadId} was not found"
                return dict(error=err.to_dict())
            progess_info.SizeUploaded = upload_item.get(files.SizeUploaded.__name__,0)
            main_file_id = upload_item.get(files.MainFileId.__name__)
        file_part.stream.seek(0,os.SEEK_SET)
        bff = file_part.stream.read()
        ReCompact.db_context.mongodb_file_add_chunks(
            db=app_db,
            chunk_index= progess_info.ChunkIndex,
            fs_id=main_file_id,
            data= bff

        )


        progess_info.SizeUploaded+= bff.__len__()
        progess_info.SizeUploadedInHumanReadable = humanize.filesize.naturalsize(progess_info.SizeUploaded)
        progess_info.Percent =float(round((progess_info.SizeUploaded*100)/progess_info.FileSize,2))
        status=0
        if progess_info.ChunkIndex==progess_info.NumOfChunks-1:
            status=1
        files.update_one(
            files._id == progess_info.UploadId,
            files.set(
                files.SizeUploaded==progess_info.SizeUploaded,
                files.Status==status,
                files.NumOfChunksCompleted == progess_info.ChunkIndex
            )
        )
        ret_data =progess_info.to_dict()
        #http://172.16.9.78:5012/api/files/long-test/directory/36855ade-650d-43da-9b49-fe4e8912e555/fscrawler.pdf
        #"ThumbUrl": "http://172.16.9.78:5012/api/files/hps-file-test/thumb/982c7c7f-116d-445f-b29f-6a3a3f1dea19.png"
        ret_data["RelUrlOfFile"] = f"files/{app_name}/diretory/{progess_info.UploadId}/{progess_info.FileName}"
        ret_data["UrlOfFile"]=f"files/{ret_data['RelUrlOfFile']}"
        ret_data["RelThumbUrl"] = f"files/{app_name}/thumb/{progess_info.UploadId}.png"
        ret_data["ThumbUrl"] = f"{app_config.api_url}/{ret_data['RelThumbUrl']}"

        return dict(
            data = ret_data
        )



quicky.api_add_resource(FileUploadChunk, "/files/<app_name>/upload/chunk")
