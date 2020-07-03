"""
Read Images, Video, Webcam
"""

import cv2

# Load Image
# img = cv2.imread("./resources/lena.png")

# Show image - Window name and image variable
# cv2.imshow("Output", img)

# Wait before closing the window
# 0 -> infinite time or 1000 -> 1000 milliseconds
# cv2.waitKey(0) 

# Load Video
# cap = cv2.VideoCapture("./resources/test_video.mp4")

# # While loop to go through all the frames in the video
# while True:
#     # 
#     success, img = cap.read()

#     cv2.imshow("Video", img)

#     # breaking out of the loop
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break


# Webcam
cap = cv2.VideoCapture(0)  # 0 uses default webcam

# Set height and width
cap.set(3, 640)
cap.set(4, 480)

cap.set(10, 100)

# While loop to go through all the frames in the video
while True:
    #
    success, img = cap.read()

    cv2.imshow("Video", img)

    # breaking out of the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


