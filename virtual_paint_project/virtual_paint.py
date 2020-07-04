import cv2
import numpy as np
import urllib
from urllib import request


def findColor(img, myColors, myColorValues):
    # Convert image to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    newPoints = []
    # Find all colors (if any are present in the image)
    for i, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[i], cv2.FILLED)

        if x != 0 and y != 0:
            newPoints.append([x, y, i])
    return newPoints

def getContours(img):

    _, contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # minimum threshold for area to avoid detecting noise
        if area > 500:
            # Drawing the boundaries of the detected color
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            # curve length
            peri = cv2.arcLength(cnt, True)
            # No. of corner points
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # Draw bounding box
            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2, y


def drawOnCanvas(myPoints, myColorValues):
    # Draw circles at the detected points
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]),
                   10, myColorValues[point[2]], cv2.FILLED)


# Url for the mobile camera acting as a webcam
# Reference - https://www.youtube.com/watch?v=2xcUzXataIk
url = "http://192.168.0.220:8080/shot.jpg"


# Colors picked by running "color_picker.py"
myColors = [[23, 60, 91, 255, 93, 255],
            [50, 91, 104, 255, 0, 255],
            [98, 115, 55, 190, 15, 255]]

# Color values to draw points
myColorValues = [[199, 153, 84],
                [21, 255, 224],
                 [113, 204, 46]]

# The detected points [Trace of the pen for drawing]
myPoints = []  # [x_, y_, colorID_]


while True:

    # Open the url and convert the image into openCV format
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    img = cv2.resize(img, (500, 300))

    imgResult = img.copy()

    # Find points
    newPoints = findColor(img, myColors, myColorValues)

    # Update detected points [update trace]
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    # Draw detected points
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Video", imgResult)

    if ord('q') == cv2.waitKey(1):
        exit(0)
