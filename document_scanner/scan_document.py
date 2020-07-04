import cv2
import numpy as np
import urllib
from urllib import request


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def preprocess(img):

    # Convert to Grayscale and add Gaussian Blur
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 1)

    # Detect Edges
    img = cv2.Canny(img, 200, 200)

    # To make edges visible
    # Make them a bit thicker by adding dilation
    kernel = np.ones((5,5))
    img = cv2.dilate(img, kernel, iterations=2)
    img = cv2.erode(img, kernel, iterations=1)
    return img


def getContours(img):

    biggest = np.array([])
    maxArea = 0

    _, contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # minimum threshold for area to avoid detecting noise
        if area > 6000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

            # curve length
            peri = cv2.arcLength(cnt, True)
            # No. of corner points
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # print(len(approx), area, maxArea)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 30)
    return biggest

def reOrder(myPoints):
    # To determine the order of the points to correctly warp the image

    # biggest shape - (4,1,2) - dim 1 is redundant
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2), dtype=np.int32)

    sums = myPoints.sum(axis = 1)

    myPointsNew[0] = myPoints[np.argmin(sums)]
    myPointsNew[-1] = myPoints[np.argmax(sums)]

    diffs = np.diff(myPoints, axis=1)

    myPointsNew[1] = myPoints[np.argmin(diffs)]
    myPointsNew[2] = myPoints[np.argmax(diffs)]

    return myPointsNew

    
def getWarp(img, biggest):

    biggest = reOrder(biggest)

    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [WIDTH, 0], [0, HEIGHT], [WIDTH, HEIGHT]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (WIDTH, HEIGHT))

    return imgOutput


            
# Url for the mobile camera acting as a webcam
# Reference - https://www.youtube.com/watch?v=2xcUzXataIk
URL = "http://192.168.0.220:8080/shot.jpg"

WIDTH = 640
HEIGHT = 480

while True:

    # Open the url and convert the image into openCV format
    imgResp = urllib.request.urlopen(URL)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    img = cv2.resize(img, (WIDTH, HEIGHT))

    imgContour = img.copy()

    imgThresh = preprocess(img)
    
    biggest = getContours(imgThresh)

    imgWarped = getWarp(img, biggest)



    hStack = stackImages(0.6, [img, imgContour, imgWarped])
    cv2.imshow("Stacked", hStack)

    if ord('q') == cv2.waitKey(1):
        exit(0)
