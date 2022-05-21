from moviepy.editor import *
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import io
import matplotlib
def video_create_thumb(in_put,scale_witdh,scale_height,second=5):
    clip= VideoFileClip(
        in_put
    )
    clip = clip.subclip(0, 5)
    frame = clip.get_frame(0)
    height,width,_ = frame.shape
    rate = scale_witdh/width # Mac dinh la bop theo chieu rong
    if height>width: # Nhung vi anh co chieu cao lon hon chieu rong
        rate = scale_height/height # Nen quye dinh la bop theo chieu chie doc
    new_witdth,new_height= int(width*rate),int(height*rate)
    res = cv2.resize(frame, dsize=(new_witdth,new_height)) #, interpolation=cv2.INTER_CUBIC)
    img = Image.fromarray(res, 'RGB')
    # img.save('my.png')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    ret = io.BytesIO(img_byte_arr)
    return ret