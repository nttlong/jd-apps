# use this command to install open cv2
# pip install opencv-python

# use this command to install PIL
# pip install Pillow
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from .thread_comunicator import ThreadCommunicator, hooker


def detect_text_block_in_doc(image_path, communicator: ThreadCommunicator == None):
    """

    :param image_path:
    :param communicator:
    :return:
    """
    master_action = 'imgae_get_all_region'
    image = None
    if communicator and not issubclass(type(communicator), ThreadCommunicator):
        raise Exception('communicator must inhertot from ThreadCommunicator')
    _communicator: ThreadCommunicator = communicator
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/read_image",
            data=dict(
                file=image_path
            ),
            status=0
        )
    im = cv2.imread(image_path, 0)

    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/read_image",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/gray_color",
            data=dict(
                file=image_path
            ),
            status=0
        )

    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/gray_color",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/GaussianBlur",
            data=dict(
                file=image_path
            ),
            status=0
        )

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    im = clahe.apply(im)
    blur = im
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/GaussianBlur",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/adaptiveThreshold",
            data=dict(
                file=image_path
            ),
            status=0
        )
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/adaptiveThreshold",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/getStructuringElement",
            data=dict(
                file=image_path
            ),
            status=0
        )
    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/getStructuringElement",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/dilate",
            data=dict(
                file=image_path
            ),
            status=0
        )
    dilate = cv2.dilate(thresh, kernel, iterations=4)
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/dilate",
            data=dict(
                file=image_path
            ),
            status=1
        )
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/findContours",
            data=dict(
                file=image_path
            ),
            status=0
        )
    # cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if _communicator:
        _communicator.post_message(
            action=f"{master_action}/findContours",
            data=dict(
                file=image_path
            ),
            status=1
        )
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area>1500:

            x, y, w, h = cv2.boundingRect(c)
            print(area,h,w)
            # if y >= 600 and x <= 1000:
            #     if area > 10000:
            #         image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
            #         line_items_coordinates.append([(x, y), (2200, y + h)])
            #     # else:
            #     #     image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
            #     #     line_items_coordinates.append([(x, y), (2200, y + h)])
            #
            # elif y >= 2400 and x <= 2000:
            #     image = cv2.rectangle(im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
            #     line_items_coordinates.append([(x, y), (2200, y + h)])
            # else:
            #     image = cv2.rectangle(im, (x, y), (x+w, y + h), color=(255, 0, 255), thickness=3)
            #     line_items_coordinates.append([(x, y), (x+w, y + h)])
            # image = cv2.rectangle(im, (x, y), (x + w, y + h), color=(255, 0, 255), thickness=3)
            if h>50 and w>50:
                line_items_coordinates.append([(x, y), (x + w, y + h)])
    return image, line_items_coordinates
