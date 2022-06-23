from text_pytesseract_open_cv.thread_comunicator import ThreadCommunicator
from text_pytesseract_open_cv.pdf_converter import to_image

comunicator = ThreadCommunicator()
to_image(
    path_to_pdf_file=r'C:\dj-apps-2022-05-25\jd-apps\data_test\taphuan.pdf',
    image_output_dir=r'C:\dj-apps-2022-05-25\jd-apps\data_test\images',
    communicator=comunicator,
    poppler_path=r'C:\dj-apps-2022-05-25\jd-apps\poppler-22.07.0\poppler-22.07.0\poppler'

)
print(comunicator)

