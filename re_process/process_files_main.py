import datetime

g_id = datetime.datetime.now().isoformat('-')


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

import consumers.file_services_upload_thumb_pdf

consumer_files_services_upload_thumb_pdf = consumers.file_services_upload_thumb_pdf.consumer
"""
Xử lý ảnh thumb cho các file office
"""
import consumers.files_services_upload_thumb_office

consumer_files_services_upload_thumb_office = consumers.files_services_upload_thumb_office.consumer

"""
Xử lý ảnh thumb video
"""
import consumers.files_services_upload_thumb_video

consumer_files_services_upload_thumb_video = consumers.files_services_upload_thumb_video.consumer

"""
Xử lý ảnh thumb cho video
"""

import consumers.files_services_upload_elastic

consumer_files_services_upload_elastic = consumers.files_services_upload_elastic.consumer

"""
Ghi nhận nôi dung vào ElasticSearch
"""

import consumers.files_services_upload_ocr_pdf

consumer_files_services_upload_ocr_pdf = consumers.files_services_upload_ocr_pdf.consumer

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



