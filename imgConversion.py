import base64
import cv2
import numpy as np

def EncodeImg(img):
    with open(img, "rb") as imageFile:
        str = base64.b64encode(imageFile.read())
        print(str)  
        return str

def DecodeImg(str):
        imgdata = base64.b64decode(str)
        filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
                f.write(imgdata)
