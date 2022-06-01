from flask import Response, request
import db_connection
import mimetypes
import api_models.Model_Files  # model file upload
import quicky
import api_models.Model_Files
import ReCompact.db_context
import mimetypes
import flask_streaming.grid_fs_stream
from flask import request,Response
cnn = db_connection.connection


def thumb(app_name, file_id):
    """
    Tải nội dung xuốn trình duyệt
    :param app_name:
    :param directory:
    :return:
    """
    import os
    id,ext = file_id.split('.')
    mime_type,_ = mimetypes.guess_type(file_id)

    files = api_models.Model_Files.DocUploadRegister(cnn,app_name)
    file_object = files.find_one(files._id == id)
    fs = ReCompact.db_context.get_mongodb_file_by_file_id(cnn.get_database(app_name),
                                                          file_object[files.ThumbFileId.__name__])
    if not fs:
        return Response(status=404)
    return  flask_streaming.grid_fs_stream.streaming_content(fs,mime_type,request,fs.length,0)

    # app_config = quicky.get_app().app_config
    # import ReCompact.db_context
    # files = api_models.Model_Files.DocUploadRegister(cnn, app_name)
    # if directory.startswith("directory/"):
    #     directory = directory["directoty".__len__() + 1:]
    # file_item = files.find_one(files.FullFileName == directory.lower())
    # if file_item is None:
    #     return Response(status=404)
    # fs = None
    # if file_item.get("MainFileId", None) is not None:
    #     fs = ReCompact.db_context.get_mongodb_file_by_file_id(
    #         file_id=file_item["MainFileId"],
    #         db=cnn.get_database(app_name)
    #
    #     )
    # else:
    #     fs = ReCompact.db_context.get_mongodb_file_by_file_name(
    #         file_name=file_item["ServerFileName"],
    #         db=cnn.get_database(app_name)
    #
    #     )
    #     files.update_one(
    #         files.ServerFileName == file_item["ServerFileName"],
    #         files.set(
    #             files.MainFileId == fs._id
    #         )
    #     )
    # if fs is None:
    #     return Response(status=404)
    # else:
    #     mime_type, _ = mimetypes.guess_type(directory)
    #     import flask_streaming.grid_fs_stream
    #     return flask_streaming.grid_fs_stream.streaming_content(
    #         mime_type=mime_type,
    #         request=request,
    #         fs=fs,
    #         streaming_segment_size_in_KB=app_config.media.streaming_segment_size_in_KB,
    #         streaming_buffering_in_KB=app_config.media.streaming_buffering_in_KB
    #
    #     )


quicky.add_api_handler('/files/<app_name>/thumb/<file_id>', endpoint=__name__, handler=thumb)
