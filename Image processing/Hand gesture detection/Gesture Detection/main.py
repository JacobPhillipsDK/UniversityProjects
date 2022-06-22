import numpy as np
import cv2

# define a video capture object
cap = cv2.VideoCapture(0)

def empty():
    pass

####### HSV BARS #######
# Kode: https://www.youtube.com/watch?v=WQeoO7MI0Bs
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)

# Reading the video file until finished
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()


    # if video finished or no Video Input
    if not ret:
        break

    # Our operations on the frame come here
    gray = frame

    ####### HSV BARS #######
    h_min = cv2.getTrackbarPos("Hue min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val max", "Trackbars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(frame, lower, upper)

    # resizing the frame size according to our need
    gray = cv2.resize(gray, (500, 500))

    # displaying the frame with fps
    cv2.imshow("frame", frame)

    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2HSV)

    cappedFrame = mask[0:500, 0:500]

    cv2.imshow("frame2", cappedFrame)

    # press 'Q' if you want to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# Destroy the all windows now
cv2.destroyAllWindow()