import cv2
import numpy as np
import os
from collections import deque
import crowncount
import result

# Root to the folder with assets
root = os.path.abspath(os.getcwd())
path_to_data = os.path.join(root, "croppedboards")
imgs = os.listdir(path_to_data)

# Array-koordinater for identificering af brikker
ArrayCords = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
FireCords = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
saveBrick = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
saveCrown = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# CrownCords holds a 5x5 array matched to the board with the crowns positions
crownCords = []

def plus(iteration):
    saveBrick[iteration] += 1

def getSavebrick(iteration):
    print("SAVED BRICKS:")
    print(saveBrick[1], saveBrick[2], saveBrick[3], saveBrick[4], saveBrick[5], saveBrick[6], saveBrick[7], saveBrick[8], saveBrick[9], saveBrick[10], saveBrick[11], saveBrick[12], saveBrick[13], saveBrick[14], saveBrick[15], saveBrick[16], saveBrick[17], saveBrick[18], saveBrick[19], saveBrick[20], saveBrick[21], saveBrick[22], saveBrick[23], saveBrick[24], saveBrick[25])
    return saveBrick[iteration]

def plusCrown(iteration, number):
    saveCrown[iteration] += number

def getSavecrown(iteration):
    print("SAVED CROWNS:")
    print(saveCrown)
    return saveCrown[iteration]

# Queue controls the amount of ongoing processes in fireSearch
queue = deque([])

# FireSearch searches for the areas of each brick type
def fireSearch(x1,y1, brickType, iteration ,startX,startY):
    # Appends the queue when a new process is started
    queue.append(1)
    saveBrick = 0
    saveBrick = getSavebrick(iteration)

    # If the amount of bricks saved for the segment is empty and the area haven't been burned by the fireSearch:
    # Initialize the bricktype to the start of the new brick area
    if saveBrick == 0 and FireCords[startX][startY] == 0:
        brickType = ArrayCords[startX][startY]

    # If the current brick haven't been burned; continue the program
    if FireCords[x1][y1] == 0:
        # Pluses the current segment brickCount with 1; inorder to find the total amount of bricks in the section
        plus(iteration)
        # Check if there is a crown on the brick
        plusCrown(iteration, crownCords[x1][y1])
        # Burns the tile of, since the program should not search the program again
        FireCords[x1][y1] = 1

        # The if-statements are made to ensure the code doesn't exceed the programs array boundaries
        # If the program finds a neighbor brick with the same brick type, it starts a new process
        if x1 == 4 and y1 == 4:
            if ArrayCords[x1-1][y1] == brickType:
                fireSearch(x1 - 1, y1, brickType, iteration, startX, startY)
        if x1 < 4:
            if ArrayCords[x1 + 1][y1] == brickType:
                fireSearch(x1 + 1,y1,brickType, iteration,startX,startY)
            if x1 > 0:
                if ArrayCords[x1 -1][y1] == brickType:
                    fireSearch(x1 - 1, y1, brickType, iteration, startX, startY)

        if x1 == 4 and y1 < 4:
            if ArrayCords[x1][y1+1] == brickType:
                fireSearch(x1,y1+1,brickType, iteration,startX,startY)
            if y1 > 0:
                if ArrayCords[x1][y1 - 1] == brickType:
                    fireSearch(x1, y1 - 1, brickType, iteration, startX, startY)
            if ArrayCords[x1 - 1][y1] == brickType:
                fireSearch(x1 - 1, y1, brickType, iteration, startX, startY)
        if y1 < 4:
            if ArrayCords[x1][y1 + 1] == brickType:
                fireSearch(x1,y1+1,brickType, iteration,startX,startY)
                if y1 > 0:
                    if ArrayCords[x1][y1 - 1] == brickType:
                        fireSearch(x1, y1 - 1, brickType, iteration, startX, startY)
    # When the process is done, pop the queue to inform that the method is not running anymore
    queue.pop()


for path in imgs:
    # For-loop with a length of total board images
    # Reads the current board image and converts it to HSV
    img = cv2.imread(os.path.join(path_to_data, path))
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("Board", img)

    # The different HSV-thresholds for the brick types
    blackLower = np.array([10, 10, 0])
    blackUpper = np.array([50, 50, 50])
    desertLower = np.array([0, 0, 0])
    desertUpper = np.array([90, 83, 82])
    forestLower = np.array([44, 70, 0])
    forestUpper = np.array([86, 255, 255])
    grassLower = np.array([30, 30, 100])
    grassUpper = np.array([85, 255, 255])
    sandLower = np.array([20, 0, 180])
    sandUpper = np.array([40, 255, 255])
    waterLower = np.array([90, 0, 100])
    waterUpper = np.array([140, 255, 255])

    # Creates a mask to hold the different threshold values
    maskMain = cv2.inRange(HSV, desertLower,desertUpper)

    # X and Y are the coordinates the program uses to know where it is in the 5x5 array
    x = 0
    y = 0

    # Integer holders for holding the amount of threshold values found and later compares them to each other to find the
    # most precise result
    waterHolder = 0
    sandHolder = 0
    grassHolder = 0
    forestHolder = 0
    desertHolder = 0
    blackHolder = 0

    # For-loop searching every brick on the board
    for z in range(25):
        if x == 5:
            x = 0
            y = y + 1

        # Creates a region of interest
        cappedFrame = maskMain[(100 * y):((100 * y) + 100), (100 * x):((100 * x) + 100)]

        # Integer holder for the amount of white pixels found in the threshold
        whitePixels = 0

        # Set-up af HSV thresholds
        for programState in range(6):
            if programState == 0:   maskMain = cv2.inRange(HSV, waterLower, waterUpper)
            if programState == 1:   maskMain = cv2.inRange(HSV, sandLower, sandUpper)
            if programState == 2:   maskMain = cv2.inRange(HSV, grassLower, grassUpper)
            if programState == 3:   maskMain = cv2.inRange(HSV, forestLower, forestUpper)
            if programState == 4:   maskMain = cv2.inRange(HSV, desertLower, desertUpper)
            if programState == 5:   maskMain = cv2.inRange(HSV, blackLower, blackUpper)

            # Updates region of interest
            cappedFrame = maskMain[(100 * y):((100 * y) + 100), (100 * x):((100 * x) + 100)]

            # Searches the threshold for white pixel values
            for y1, row in enumerate(cappedFrame):
                for x1, v in enumerate(row):
                    if cappedFrame[y1, x1] == 255:
                        whitePixels = whitePixels + 1

            # Moves the data out of the for-loop inorder to store it
            if programState == 0:   waterHolder = whitePixels
            if programState == 1:   sandHolder = whitePixels
            if programState == 2:   grassHolder = whitePixels
            if programState == 3:   forestHolder = whitePixels
            if programState == 4:   desertHolder = whitePixels
            if programState == 5:   blackHolder = whitePixels
            whitePixels = 0

        # Print the threshold values for each brick type
        print("Sand: "+str(sandHolder) + " Water: "+str(waterHolder) + " Grass: "+str(grassHolder)+ " Forest: "+str(forestHolder)+ " Desert: "+str(desertHolder)+ " Black: "+str(blackHolder))

        # Compare all the threshold values, to find the best match
        if (sandHolder > waterHolder and sandHolder > grassHolder and sandHolder > forestHolder and sandHolder > desertHolder and sandHolder > blackHolder):
            print("Sand has the most pixels")
            ArrayCords[y][x]= 0

        if (waterHolder > sandHolder and waterHolder > grassHolder and waterHolder > forestHolder and waterHolder > desertHolder and waterHolder > blackHolder):
            print("Water has the most pixels")
            ArrayCords[y][x]= 1

        if (grassHolder > waterHolder and grassHolder > sandHolder and grassHolder > forestHolder and grassHolder > desertHolder and grassHolder > blackHolder):
            print("Grass has the most pixels")
            ArrayCords[y][x]= 2

        if (forestHolder > waterHolder and forestHolder > sandHolder and forestHolder > grassHolder and forestHolder > desertHolder and forestHolder > blackHolder):
            print("Forest has the most pixels")
            ArrayCords[y][x]= 3

        if (desertHolder > waterHolder and desertHolder > sandHolder and desertHolder > grassHolder and desertHolder > forestHolder and desertHolder > blackHolder):
            print("Desert has the most pixels")
            ArrayCords[y][x] = 4

        if (blackHolder > waterHolder and blackHolder > sandHolder and blackHolder > grassHolder and blackHolder > forestHolder and blackHolder > desertHolder):
            print("Black has the most pixels")
            ArrayCords[y][x] = 5

        sandHolder=0
        waterHolder=0
        grassHolder=0
        forestHolder=0
        desertHolder=0
        blackHolder=0

        # Moves the for-loop on tile to the right
        x = x + 1

    counter = 0
    counterX = 0
    counterY = 0

    # Resets the arrays after analysing the data
    for i in range(len(saveBrick)):
        saveBrick[i] = 0
        saveCrown[i] = 0
    for i in range(len(FireCords)):
        for m in range(len(FireCords)):
            FireCords[i][m] = 0

    # Calls the crowncount.py file to return the crown array
    crownCords = crowncount.finder()

    # FireSearching caller, gets called while the counter is below 25 (The total amount of bricks)
    while ((len(queue) < 1) and (counter < 25)):
        counter += 1
        print ("COUNTER: "+str(counter))
        fireSearch(counterX,counterY,0,counter, counterX,counterY)
        counterX += 1
        if counter % 5 == 0:
            counterY += 1
            counterX = 0

    print("ARRAYCORDS")
    for m in range(5):
        print(ArrayCords[m])
    print("CROWNCORDS")
    for i in range(len(crownCords)):
        print(crownCords[i])
    print(saveBrick)
    print(saveCrown)
    result.calculateResult(saveBrick, saveCrown)

    cv2.waitKey(0)
