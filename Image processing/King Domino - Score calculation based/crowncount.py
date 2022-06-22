import cv2
import numpy as np
import os

root = os.path.abspath(os.getcwd())
path_to_data = os.path.join(root, "croppedboards")
imgs = os.listdir(path_to_data)
color = 255, 100, 203


def finder():
    for path in imgs:
        # Crown count is a 15x15 array containing all the possible coordinates for the crowns on all bricks
        crownCount = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # Array which later compresses crownCount from a 15x15 array to a 5x5 array
        crownCompressed = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        img = cv2.imread(os.path.join(path_to_data, path))
        # Converts the images to gray scale inorder to compare the images
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Read and compare the templates
        for i in range(1, 130):
            # String holders getting initialized with different names each for-loop
            templateStrHolder, resStrHold, locStrHold = ("temp" + str(i)), ("res" + str(i)), ("loc" + str(i))
            templateHolder = cv2.imread(("Template Images/" + templateStrHolder + ".png"), 0)

            # Store width in variable w and height in variable h of template
            heightStrHold, widthStrHold = ("height" + str(i)), ("width" + str(i))
            heightStrHold, widthStrHold = templateHolder.shape[::-1]

            # Now we perform match operations
            resStrHold = cv2.matchTemplate(img_gray, templateHolder, cv2.TM_CCOEFF_NORMED)

            # Declares the threshold value
            threshold = 0.86

            # Store the coordinates of matched region in a numpy array
            locStrHold = np.where(resStrHold >= threshold)
            for pt in list(zip(*locStrHold[::-1])):
                cv2.rectangle(img, pt, (pt[0] + widthStrHold, pt[1] + heightStrHold), color, 2)
                MatchTemp = (pt[0] + widthStrHold, pt[1] + heightStrHold)
                for y in range(16):
                    for x in range(16):
                        if (pt[0] <= y * (33.333)) & (pt[0] >= (y - 1) * (33.333)):
                            if (pt[1] <= x * (100 / 3)) & (pt[1] >= (x - 1) * (100 / 3)):
                                if crownCount[x - 1][y - 1] == 0:
                                    crownCount[x - 1][y - 1] += 1

        cv2.imshow('Results' + root, img)

        # Compresses the 15x15 array to a 5x5 array
        for y in range(5):
            for x in range(5):
                sectionCount = (crownCount[y * 3][x * 3]) + (crownCount[y * 3][x * 3 + 1]) + (
                    crownCount[y * 3][x * 3 + 2]) + (crownCount[y * 3 + 1][x * 3]) + (
                                   crownCount[y * 3 + 1][x * 3 + 1]) + (
                                   crownCount[y * 3 + 1][x * 3 + 2]) + (crownCount[y * 3 + 2][x * 3]) + (
                                   crownCount[y * 3 + 2][x * 3 + 1]) + (crownCount[y * 3 + 2][x * 3 + 2])
                crownCompressed[y][x] = sectionCount

        print("UNCOMPRESSED")
        for x in range(len(crownCount)):
            print(crownCount[x])

        print("COMPRESSED")
        for x in range(len(crownCompressed)):
            print(crownCompressed[x])

        return crownCompressed
        cv2.waitKey(0)
