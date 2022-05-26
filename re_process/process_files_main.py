from numpy.f2py.auxfuncs import throw_error

import re_process.config
import datetime

g_id = datetime.datetime.now().isoformat('-')
import ReCompact_Kafka.consumer


def on_error(err, msg):
    print(err)
    print(msg)


import files_process_handlers.files_services_upload

consumer_files_services_upload = files_process_handlers.files_services_upload.consumer
"""
Tiếp nhận topic và raise event đây là consumer chính\n
Hoạt động:
    khi nhận được topic "files.services.upload"\n
    consumer này sẽ tùy theo file mà trigger các sự kiện khác
"""

import files_process_handlers.file_services_upload_thumb_pdf

consumer_files_services_upload_thumb_pdf = files_process_handlers.file_services_upload_thumb_pdf.consumer
"""
Xử lý ảnh thumb cho các file office
"""
import files_process_handlers.files_services_upload_thumb_office

consumer_files_services_upload_thumb_office = files_process_handlers.files_services_upload_thumb_office.consumer

"""
Xử lý ảnh thumb video
"""
import files_process_handlers.files_services_upload_thumb_video

consumer_files_services_upload_thumb_video = files_process_handlers.files_services_upload_thumb_video.consumer

"""
Xử lý ảnh thumb cho video
"""

import files_process_handlers.files_services_upload_elastic

consumer_files_services_upload_elastic = files_process_handlers.files_services_upload_elastic.consumer

"""
Ghi nhận nôi dung vào ElasticSearch
"""

import files_process_handlers.files_services_upload_ocr_pdf

consumer_files_services_upload_ocr_pdf = files_process_handlers.files_services_upload_ocr_pdf.consumer

"""
Xử lý OCR
"""

"""
Khởi động các consumer thứ cấp
"""

consumer_files_services_upload_ocr_pdf.start_and_join()
consumer_files_services_upload_elastic.start_and_join()
consumer_files_services_upload_thumb_video.start_and_join()
consumer_files_services_upload_ocr_pdf.start_and_join()
consumer_files_services_upload_thumb_office.start_and_join()

consumer_files_services_upload.run()
"""
Chạy consumer chính
"""



