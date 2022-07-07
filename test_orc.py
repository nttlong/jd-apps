from text_pytesseract_open_cv.thread_comunicator import ThreadCommunicator
from text_pytesseract_open_cv.pdf_converter import to_image
from text_pytesseract_open_cv.pdf_region import  detect_text_block_in_doc
from text_pytesseract_open_cv.ocr import  ocr

comunicator = ThreadCommunicator()
# dir,files = to_image(
#     path_to_pdf_file=r'C:\dj-apps-2022-05-25\jd-apps\data_test\0002.pdf',
#     image_output_dir=r'C:\dj-apps-2022-05-25\jd-apps\data_test\images',
#     communicator=comunicator,
#
# )
img_path=f"C:\dj-apps-2022-05-25\jd-apps\data_test\im-002.png"
img_path=f"C:\dj-apps-2022-05-25\jd-apps\data_test\img-004.jpg"
# img_path = files[0]
a,b= detect_text_block_in_doc(img_path,comunicator)
ocr(b,img_path)
print(comunicator)

