from text_pytesseract_open_cv.thread_comunicator import ThreadCommunicator
from text_pytesseract_open_cv.pdf_converter import to_image
from text_pytesseract_open_cv.pdf_region import  get_all_region
from text_pytesseract_open_cv.ocr import  ocr

comunicator = ThreadCommunicator()
dir,files = to_image(
    path_to_pdf_file=r'C:\dj-apps-2022-05-25\jd-apps\data_test\taphuan.pdf',
    image_output_dir=r'C:\dj-apps-2022-05-25\jd-apps\data_test\images',
    communicator=comunicator,

)

a,b= get_all_region(files[3],comunicator)
ocr(b,files[3])
print(comunicator)

