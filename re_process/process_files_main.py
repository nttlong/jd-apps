from numpy.f2py.auxfuncs import throw_error

import re_process.config
import datetime

g_id = datetime.datetime.now().isoformat('-')
import ReCompact_Kafka.consumer


def on_error(err, msg):
    print(err)
    print(msg)

"""
Tiếp nhận topic và raise event
"""
import files_process_handlers.files_services_upload

consumer_files_services_upload = ReCompact_Kafka.consumer.create(
    topic_id="files.services.upload",
    group_id=f"files.services.upload.{g_id}",
    server=re_process.config.kafka_broker,
    on_consum=files_process_handlers.files_services_upload.handler,
    on_consum_error=files_process_handlers.files_services_upload.error,

)
"""
xử lý ảnh thumb cho file pdf
"""
import files_process_handlers.file_services_upload_thumb_pdf

consumer_files_services_upload_thumb_pdf = ReCompact_Kafka.consumer.create(
    topic_id="files.services.upload.thumb.pdf",
    group_id=f"files.services.upload.thumb.pdf.{g_id}",
    server=re_process.config.kafka_broker,
    on_consum=files_process_handlers.file_services_upload_thumb_pdf.handler,
    on_consum_error=files_process_handlers.files_services_upload.error,

)
"""
Xử lý ảnh thumb cho các file office
"""
import files_process_handlers.files_services_upload_thumb_office

consumer_files_services_upload_thumb_office = ReCompact_Kafka.consumer.create(
    topic_id="files.services.upload.thumb.office",
    group_id=f"files.services.upload.thumb.office.{g_id}",
    server =re_process.config.kafka_broker,
    on_consum=files_process_handlers.files_services_upload_thumb_office.handler_use_libre_office,
    on_consum_error=files_process_handlers.files_services_upload.error,
)

th1 = consumer_files_services_upload.get_thread()
th2 = consumer_files_services_upload_thumb_pdf.get_thread()
th3 = consumer_files_services_upload_thumb_office.get_thread()
th1.start()
th2.start()
th3.start()
th1.join()
th2.join()
th3.join()
while True:
    pass
