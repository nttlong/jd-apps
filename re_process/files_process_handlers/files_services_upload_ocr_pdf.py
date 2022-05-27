"""
Lưu ý:
 Với các file đã đươc OCR có thể bị lỗi

"""
import bson
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
import re_process.mongo_db
import ReCompact_Kafka.consumer
import re_process.config
import api_models.Model_Files
import ReCompact.dbm.DbObjects
import ReCompact.db_context
import datetime
topic ="files.services.upload.ocr.pdf"
def handler(
        consumer: ReCompact_Kafka.consumer.Consumer_obj,
        msg,
        logger: logging.Logger
):
    data = consumer.get_json(msg)
    file_path = data["FilePath"]
    upload_info = data["UploadInfo"]
    app_name = data["AppName"]
    upload_id =upload_info["_id"]


    import logging
    import os
    import subprocess
    import sys
    out_put_dir = os.path.join(re_process.config.tmp_dir_ocr, app_name)
    if not os.path.isdir(out_put_dir):
        os.makedirs(out_put_dir)
    out_put_file_path = os.path.join(out_put_dir,f"{upload_id}.pdf")
    """
    Kiểm tra nôi dung file đã được ORC chưa?
    """
    fs_craller_path = os.path.join(re_process.config.fs_crawler_path,f"{upload_id}.pdf")

    # if not re_process.config.is_debug:
    import ocrmypdf
    # file_path = input = r"\\192.168.18.36\Share\00002.pdf"

    try:
        cmd = ["ocrmypdf", "--deskew", file_path, out_put_file_path]
        logger.info(f"OCR file {file_path} to {out_put_file_path}")
        logging.info(cmd)
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.communicate() #Đợi
        logger.info(f"OCR file {file_path} to {out_put_file_path} is success")
    except Exception as e:
        logger.debug(e)
    finally:
        if os.path.isfile(out_put_file_path):
                import shutil
                shutil.copy(out_put_file_path,fs_craller_path)
                db = re_process.mongo_db(app_name)
                upload_data_item = ReCompact.dbm.DbObjects.find_one_to_dict(
                    db = db,
                    data_item_type= api_models.Model_Files.DocUploadRegister,
                    filter= ReCompact.dbm.FILTER._id == upload_id
                )
                process_history = upload_info.get("ProcessHistories", [])
                process_history += [
                    api_models.Model_Files.DocUploadRegister.ProcessHistory(
                        _id= bson.ObjectId(),
                        ProcessOn=datetime.datetime.now(),
                        ProcessAction=topic,
                        UploadId=upload_id
                    )
                ]

                fs = ReCompact.db_context.create_mongodb_fs_from_file(
                    db =db,
                    full_path_to_file= out_put_file_path

                )
                ReCompact.dbm.DbObjects.update(
                    db,
                    data_item_type=api_models.Model_Files.DocUploadRegister,
                    filter=   ReCompact.dbm.FILTER._id == upload_id,
                    updator= ReCompact.dbm.SET(

                        ReCompact.dbm.FIELDS.MainFileId == fs._id,
                        ReCompact.dbm.FIELDS.OriginalFileId == upload_data_item.get("OriginalFileId"),
                        ReCompact.dbm.FIELDS.LastModifiedOn == datetime.datetime.now(),
                        ReCompact.dbm.FIELDS.DocUploadRegister.ProcessHistory ==process_history


                    )
                )

                if upload_data_item is None:
                    consumer.commit(msg)
                    return

        else:
            import shutil
            shutil.copy(file_path, fs_craller_path)
            consumer.commit(msg)

def error(err,msg,logger):
    logger.debug(err)

import uuid
__id__ = str(uuid.uuid4())
import re_process.config
import ReCompact_Kafka.consumer
consumer = ReCompact_Kafka.consumer.create(
    topic_id=topic,
    group_id=f"{topic}.{__id__}",
    server=re_process.config.kafka_broker,
    on_consum=handler,
    on_consum_error=error,
)
if __name__ == "__main__":
    consumer.run()