import cv2
import numpy as np
import math
import pytesseract
from PIL import Image
import glob
import os
import re


def removeSpecial(text):
    result = re.sub(r"[\'\.,@?$%_»«:،٬٫٭؟؛٪ـ]", "", text, flags=re.I)
    return result

def removeHamza(test):
    length=len(test)
    while (True):
        if test[length-1]=="ء":
            test = test[0:length-2]
            length=len(test)
            print(length)
        else:
            break
    return test

def prepareImg(img, height):
	"""convert given image to grayscale image (if needed) and resize to desired height"""
	assert img.ndim in (2, 3)
	if img.ndim == 3:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	h = img.shape[0]
	factor = height / h
	return cv2.resize(img, dsize=None, fx=factor, fy=factor)

def createKernel(kernelSize, sigma, theta):
    """create anisotropic filter kernel according to given parameters"""
    assert kernelSize % 2  # must be odd size
    halfSize = kernelSize // 2

    kernel = np.zeros([kernelSize, kernelSize])
    sigmaX = sigma
    sigmaY = sigma * theta

    for i in range(kernelSize):
        for j in range(kernelSize):
            x = i - halfSize
            y = j - halfSize

            expTerm = np.exp(-x ** 2 / (2 * sigmaX) - y ** 2 / (2 * sigmaY))
            xTerm = (x ** 2 - sigmaX ** 2) / (2 * math.pi * sigmaX ** 5 * sigmaY)
            yTerm = (y ** 2 - sigmaY ** 2) / (2 * math.pi * sigmaY ** 5 * sigmaX)

            kernel[i, j] = (xTerm + yTerm) * expTerm

    kernel = kernel / np.sum(kernel)
    return kernel

def detectWord(img,toDetect):
    preparedImg = prepareImg(img,600)

    if not os.path.exists('cropped'):
        os.makedirs('cropped')

    img1 = preparedImg

    kernel = createKernel(kernelSize=15, sigma=11, theta=6)
    imgFiltered = cv2.filter2D(preparedImg, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)
    imgFiltered=cv2.dilate(imgFiltered,circle_kernel,iterations=5)
    (_, imgThres) = cv2.threshold(imgFiltered, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    imgThres = 255 - imgThres

# Find the contours
    contours,hierarchy = cv2.findContours(imgThres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    minArea=250
    res = []
    for c in contours:
		# skip small word candidates
		    if cv2.contourArea(c) < minArea:
			    continue
		# append bounding box and image of word to result list
		    currBox = cv2.boundingRect(c) # returns (x, y, w, h)
		    (x, y, w, h) = currBox
		    currImg = preparedImg[y:y+h, x:x+w]
		    res.append((currBox, currImg))


    res= sorted(res, key=lambda entry:entry[0][0])
    i=0
    w, h = 5,len(res)
    Matrix = [[0 for x in range(w)] for y in range(h)]
    print('Segmented into %d words' % len(res))

    for (j, w) in enumerate(res):
        (wordBox, wordImg) = w
        (x, y, w, h) = wordBox
        yr=range(y-10,y+h+10)
        xr=range(x-5,x+w+2)
        for k in range(img1.shape[0]):
            for g in range(img1.shape[1]):
                if not( g  in xr and k in yr):
                    img1[k, g] = 255
        Matrix[i][0] = y-10
        Matrix[i][1] =y+h+10
        Matrix[i][2] =x-5
        Matrix[i][3] = x+w+2
        Matrix[i][4] = 'cropped\pic000%d.png' % (i,)
        cv2.imwrite('cropped/pic{:>05}.png'.format(i), img1)
        imgx = img
        img1 = prepareImg(img, 600)
        i += 1

    k=0
    y=toDetect

    croppedImages = glob.glob("cropped/*.png")
    for image in croppedImages:
        with open(image, 'rb') as file:
            text = pytesseract.image_to_string(Image.open(file),lang='ara',config=" --psm 10 ")
            text=removeSpecial(text)
            y=removeSpecial(y)
            text=removeHamza(text)
            y=removeHamza(y)
            if text == y:
                for t in range(len(res)):
                    if (str(image) == str(Matrix[t][4])):
                        cv2.rectangle(img1, (Matrix[t][2], Matrix[t][0]), (Matrix[t][3], Matrix[t][1]), 0, 1)
                    print(Matrix[t][4])
            print(text)
            print(image)
            k +=1

    cv2.imwrite('detected_Image.png',img1)

dot_kernel = np.ones((1,1),np.uint8)

circle_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

bigger_circle_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
bigger_circle_kernel[0][1]=1
bigger_circle_kernel[0][3]=1
bigger_circle_kernel[4][1]=1
bigger_circle_kernel[4][3]=1

img = cv2.imread('01.png')

detectWord(img,"اللوح")
