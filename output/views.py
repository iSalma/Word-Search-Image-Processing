from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import cv2
import numpy as np
import os
import argparse
import pytesseract
from PIL import Image
from tkinter import *
import json
from imgConversion import EncodeImg , DecodeImg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from Processing import *


class ProcessAPI(APIView):
    def post(self,request):
        string=request.data["img"]
        string = string.replace('\n', '')
        EncodeImg('picrb01.jpg')
        DecodeImg(string)
        arabic01 = cv2.imread('some_image.jpg',1)
        arabic_processed=arabic_processing(arabic01,False)
        # print(img)
        # return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response('Done',status=status.HTTP_200_OK)


