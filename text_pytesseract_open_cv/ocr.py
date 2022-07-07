import pytesseract
import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
def ocr(line_items_coordinates,image_path):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # load the original image
    image = cv2.imread(image_path)

    # get co-ordinates to crop the image


    # cropping image img = image[y0:y1, x0:x1]
    # img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]

    # plt.figure()


    # convert the image to black and white for better OCR
    # ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
    # plt.imshow(thresh1)
    # plt.show()
    # # pytesseract image to string to get results
    # text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    # print(text)
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(image)
    for c in line_items_coordinates:
        rect = patches.Rectangle((c[0][0], c[0][1]), c[1][0]-c[0][0],c[1][1]-c[0][1], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    # Create a Rectangle patch


    # Add the patch to the Axes


    plt.show()
    print('ok')