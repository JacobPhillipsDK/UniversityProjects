import numpy as np
import cv2

# define a video capture object
cap = cv2.VideoCapture(0)

hull = []

def empty():
    pass

webcamCap = ""

# Reading the video file until finished
frameCount = 0
frameCount = frameCount + 1
_, bg = cap.read()
top, bottom, right, left = 10, 400, 900, 1200

while True:
    ret, frame = cap.read()

    # if video finished or no Video Input
    if not ret:
        break
    ROI = bg[top:bottom, right:left]
    ROIgray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    # roi på skærmen
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    # resizing the frame size according to our need
    # BGgray = cv2.resize(bg, (500, 500))

    # displaying the frame with fps
    # cv2.imshow("frame", frame)
    grayFrameHSV = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    # grayFrameGRAY = cv2.cvtColor((grayFrameHSV, cv2.COLOR_BGR2GRAY))


    feedHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ROI2 = feedHSV[top:bottom, right:left]
    #feedGray = cv2.cvtColor(feedHSV,cv2.COLOR_BGR2GRAY)


    diff = cv2.absdiff(ROIgray,ROI2)
    cv2.imshow("frame2", diff)
    # https://www.learnopencv.com/convex-hull-using-opencv-in-python-and-c/
    blur = cv2.blur(diff, (5, 5))  # blur the image
    threshold = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("thresh", threshold)
    im2, contours, hierachy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros((threshold.shape[0], threshold.shape[1], 3), np.uint8)
    cv2.imshow("frame",frame)

    for i in range(len(contours)):
        hull.append(cv2.convexHull(contours[i], False))

    for i in range(len(contours)):
        color_contours = (0, 0, 255)
        color = (255, 0, 0)
        cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierachy)
        cv2.drawContours(drawing, hull, i, color, 1, 8)
    cv2.imshow("Convex", drawing)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        _, bg = cap.read()

# When everything done, release the capture
cap.release()
# Destroy the all windows now
cv2.destroyAllWindow()
