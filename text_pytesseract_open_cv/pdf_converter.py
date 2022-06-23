"""
Extracting Text from Scanned PDF using Pytesseract & Open CV
Package này cho phép extract text từ một file Pdf Scanned bằng các sử dụng Pytesseract và Open CV
Hiển nhiên cả tesseract  và open cv phải được cài đặt trên máy
requirements:
    pip install pdf2image
    pip install Pillow
    pip install opencv-python
"""
from pdf2image import convert_from_path
import os
import uuid
import pathlib
from .thread_comunicator import ThreadCommunicator,hooker
import glob, sys, fitz

def to_image(path_to_pdf_file: str, image_output_dir: str,poppler_path, communicator=None):
    """
    Hàm này sẽ convert file pdf ra thành các file image dạng png.
    Lưu ý một điều: một file pdf có nhiều trang, vì lẽ đó khi chuyển đổi sang file ảnh
    sẽ phát sinh rất nhiều file
    Giải pháp ở đây là ta sẽ tạo ra 1 thư mục theo quy tắc sau:
    Từ thư mục được chỉ định trong tham số image_output_dir ta sẽ tạo ra một thư mục con nằm trong đó
    mà tên của thư mục con này là một số GUI. Bên trong thư mục con này sẽ chứa tất cả các file ảnh được sinh ra

    :param comunicator:
    :param path_to_pdf_file: đường dẫn đến file pdf
    :param image_output_dir: đường dẫn đến thư mục phát sinh file ảnh
    :return: đường dẫn đến các thư mục chứa file
    """
    master_action='pdf_convert_to_image'
    if communicator and not issubclass(type(communicator),ThreadCommunicator):
        raise Exception(f"communicator must be a sub class of ThreadCommunicator")
    _communicator: ThreadCommunicator =communicator
    # if _communicator:
    #     _communicator.post_message(
    #         action=f'{master_action}/reading_pdf_file',
    #         status=0,
    #         data= dict(
    #             file=path_to_pdf_file
    #         )
    #     )

    # pages = convert_from_path(path_to_pdf_file, 350, poppler_path= poppler_path)
    # if _communicator:
    #     _communicator.post_message(
    #         action=f'{master_action}/reading_pdf_file',
    #         object_status=1,
    #         data=dict(
    #             file=path_to_pdf_file
    #         )
    #     )
    out_put_images_dir_name = str(uuid.uuid4())
    """
    Tên của thư mục chứa các file ảnh
    """
    full_path_out_put_images_dir_name = os.path.join(image_output_dir, out_put_images_dir_name).replace('/', os.sep)
    """
    Đường dẫn đầy đủ đến thư mục chứa các file
    """
    if not os.path.isdir(full_path_out_put_images_dir_name):
        os.makedirs(full_path_out_put_images_dir_name)
    pdf_filename_only = pathlib.Path(path_to_pdf_file).stem
    """
    Tên của file pdf không có phần mở rộng
    """
    i = 1
    if _communicator:
        _communicator.post_message(
            action=f'{master_action}/convert_pdf_file_to_image',
            status=0,
            data=dict(
                file=path_to_pdf_file
            )
        )
    mat = fitz.Matrix(300 / 72, 300 / 72)
    doc = fitz.open(path_to_pdf_file)  # open document
    i=0
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image

        image_name = f"{pdf_filename_only}[{i}].png"
        full_path_to_image = os.path.join(full_path_out_put_images_dir_name, image_name).replace('/', os.sep)
        if _communicator:
            _communicator.post_message(
                action=f'{master_action}/convert_pdf_file_to_image/page/{i}',
                status=0,
                data=dict(
                    file=full_path_to_image
                )
            )
        pix.save(full_path_to_image)  # store image as a PNG

        if _communicator:
            _communicator.post_message(
                action=f'{master_action}/convert_pdf_file_to_image/page/{i}',
                status=1,
                data=dict(
                    file=full_path_to_image
                )
            )
        i = i + 1

    if _communicator:
        _communicator.post_message(
            action=f'{master_action}/convert_pdf_file_to_image',
            status=1,
            data=dict(
                file=path_to_pdf_file
            )
        )
    return full_path_out_put_images_dir_name
