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
api_models.Model_Files.DocUploadRegister.NumOfChunksCompleted
cnn = db_connection.connection
app_config = quicky.get_app().app_config
"""
Cấu hình app đang chạy
"""

@quicky.object_contraints.contraints()
class FileProgressInfo:
    """
    Thông tin xử lý
    Mục đích của bản ghi này là ghi nhận quá trình upload,
    Và sẽ được sử dụng lại khi user muốn resume upload
    """
    UploadId =(str,True)
    """
    Quan trọng đây là Id upload số Guid tự động phát sinh
    """

    FileName = (str, True)
    SizeInHumanReadable = (str, True)
    """
    Kích thước file quy ra chuỗi cho dễ đọc
    """
    NumOfChunks = (int, True)

    ChunkSizeInBytes = (int, True)
    """
    Kích thước phân đoạn tính bằng byte
    """
    NumOfChunksCompleted = (int, True)
    """
    Số chunk đã upload thành công
    """
    Percent=(float,True)
    """
    Tỉ lệ upload
    """
    SizeUploadedInHumanReadable=(str,True)
    """
    Kích thước đã upload xong quy ra chuỗi
    """

    SizeUploaded = (float,True)
    """
    Kích thước đã upload xong
    """
    FileExt = (str,True)
    """
    Phần mở rộng file
    """
    ServerFileName = (str,True)
    """
    Tên file sẽ lưu ở server
    """
    MimeType =(str,True)
    FullFileName =(str,True)
    Status=(int,True)
    RegisterOn =(datetime.datetime,True)
    RegisterBy = (str, True)
    FileSize = (int, True)
    ChunkSizeInKB= (int, True)
    IsPublic=(bool,True)
    ChunkIndex=(int,True)
    """
    Rất quan trọng nếu lỗi dùng để resume upload
    """


@quicky.object_contraints.contraints()
class FileRegisterInfo:
    """
    Dùng để nhận các params gởi từ client cho file upload
    """
    FileName = (str, True)
    """
    tên file kiểu text bắt buộc
    """
    FileSize = (int, True)
    """
    Kích thước file kiểu số bắt buộc
    """
    ChunkSizeInKB = (int, True)
    """
    Phân đoạn
    """
    IsPublic = (bool, True)
    """
    Chế độ 
    """
    Description = (str)


class FileRegister(Resource):
    """
    Upload controller
    """

    def post(self, app_name):

        """
        Lúc đăng ký upload đi về đây
        :param app_name:
        :return:
        """
        data = FileRegisterInfo(request.get_json(force=True))
        """
        Thông tin nhận được
        """
        err = data.get_error()
        """
        Lỗi lúc parse
        """
        if err:
            """
            Trả lỗi
            """
            return dict(
                error=err.to_dict()
            )
        # Bắt đầu xử lý
        chunk_size = data.ChunkSizeInKB * 1024
        """
        Độ dài của chunk tính bằng bytes
        """
        size_in_human_readalbe = humanize.filesize.naturalsize(data.FileSize)
        """
        Kích thước của file quy ra text
        """
        num_of_chunks = int(data.FileSize / chunk_size)
        mime_type,_ = mimetypes.guess_type(data.FileName)
        filename_only, file_extension = os.path.splitext(data.FileName)
        upload_id = str(uuid.uuid4())
        if data.FileSize % chunk_size > 0:
            num_of_chunks += 1
        ret_data = {
            FileProgressInfo.UploadId: upload_id,
            FileProgressInfo.FileName: data.FileName,
            FileProgressInfo.NumOfChunksCompleted: 0,
            FileProgressInfo.ChunkSizeInBytes: chunk_size,
            FileProgressInfo.NumOfChunks: num_of_chunks,
            FileProgressInfo.Percent: float(0),
            FileProgressInfo.SizeUploadedInHumanReadable: humanize.naturalsize(0),
            FileProgressInfo.SizeUploaded: float(0),
            FileProgressInfo.MimeType: mime_type,
            FileProgressInfo.FileExt: file_extension,
            FileProgressInfo.SizeInHumanReadable:size_in_human_readalbe,
            FileProgressInfo.ServerFileName : f"{upload_id}.{file_extension}",
            FileProgressInfo.FullFileName : f"{upload_id}/{data.FileName.lower()}",
            FileProgressInfo.Status:0,
            FileProgressInfo.RegisterOn:datetime.datetime.now(),
            FileProgressInfo.RegisterBy:app_name,
            FileProgressInfo.FileSize: data.FileSize,
            FileProgressInfo.ChunkSizeInKB: data.ChunkSizeInKB,
            FileProgressInfo.IsPublic: data.IsPublic,
            FileProgressInfo.ChunkIndex:int(0)



            }
        ret_data={**ret_data,**{"_id":upload_id}}
        file_progress_info = FileProgressInfo(ret_data)
        err = file_progress_info.get_error()
        """
        Kiểm tra lỗi
        """
        if err:
            """
            lỗi này không thông báo cho người dùng, thuộc về lỗi logic
            """
            app_config.logger.debug(err.as_exception())
            if app_config.debug:
                """
                Nếu đang ở chế độ debug
                """
                raise err.as_exception()
            else:
                return Response(status=500)

        files = api_models.Model_Files.DocUploadRegister(cnn,app_name)
        """
        Tạo queryable file cho MongoDb
        """
        try:
            files.insert_one(file_progress_info.to_dict())
            return dict(
                data=file_progress_info.to_dict()
            )
        except Exception as e:
            print(e)


quicky.api_add_resource(FileRegister, "/files/<app_name>/upload/register")
