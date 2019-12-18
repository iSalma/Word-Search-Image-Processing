

import cv2
import numpy as np
import math
from skimage.io import imread
from skimage.color import rgb2gray
from scipy import signal as sig
import pytesseract
from PIL import Image
import glob
import os

img = cv2.imread('words.png')
os.makedirs("gg")
print( pytesseract.image_to_string(Image.open('words.png')))


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

kernel1 = np.ones((5,5), np.uint8)
# # apply filter kernel
#
#
img = prepareImg(img,600)
img1 =img
#cv2.imshow('i',img)
img = cv2.erode(img, kernel1, iterations=1)
img = cv2.dilate(img, kernel1, iterations=1)
cv2.imshow('im77',img)
kernel = createKernel(kernelSize=21, sigma=11, theta=7)
imgFiltered = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REPLICATE).astype(np.uint8)
cv2.imshow('im4',img)
(_, imgThres) = cv2.threshold(imgFiltered, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
imgThres = 255 - imgThres
#
# cv2.imshow('imd',imgThres)
#
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
		currImg = img[y:y+h, x:x+w]
		res.append((currBox, currImg))


res= sorted(res, key=lambda entry:entry[0][0])

i=0

w, h = 5, len(res);
Matrix = [[0 for x in range(w)] for y in range(h)]
print('Segmented into %d words' % len(res))
for (j, w) in enumerate(res):
    (wordBox, wordImg) = w
    (x, y, w, h) = wordBox
    # cv2.rectangle(img1, (x, y), (x + w, y + h), 0, 1)
    crop_img = img1[y:y + h, x:x + w]
    Matrix[i][0] = y
    Matrix[i][1] =y+h
    Matrix[i][2] =x
    Matrix[i][3] = x+w
    Matrix[i][4] = 'gg/pic000%d.jpg' % (i,)
    print(Matrix[i][4])
    #cv2.imshow('pic{:>05}.jpg'.format(i), crop_img)


    #cv2.imwrite('gg/pic{:>05}.jpg'.format(i), crop_img)

    i += 1

images = glob.glob("gg/*.jpg")
k=0
arr=[]
y ="hate"

for image in images:
    with open(image, 'rb') as file:

        text = pytesseract.image_to_string(Image.open(file),config='--psm 10')
        if text==y :
            #for j in range(len(res)):
             for t in range(len(res)):
               if(str(image) ==str(Matrix[t][4])):
                 cv2.rectangle(img1, (Matrix[t][2],  Matrix[t][0]), (Matrix[t][3],Matrix[t][1]), 0, 1)
                 print(Matrix[t][4])
            #img1[Matrix[k][0]:Matrix[k][1], Matrix[k][2]:Matrix[k][3]]=[]
        print(text)
        print(image)
        k +=1

cv2.imshow('im',img1)

# for cnt in contours:
#     x,y,w,h = cv2.boundingRect(cnt)
#     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#     cv2.rectangle(thresh_color,(x,y),(x+w,y+h),(0,255,0),2)
#     crop_img = img[y:y + h, x:x + w]
#     #cv2.imwrite('pic{:>05}.jpg'.format(i), crop_img)
#     #cv2.imshow('pic{:>05}.jpg'.format(i), crop_img)
#     i+=1

#cv2.imshow('img',img)
#cv2.imshow('res',thresh_color)

cv2.waitKey(0)



