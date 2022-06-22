def calculateResult (cardSegments, crownSegments):
    totalResult = 0
    print("\n\n\n\nData:")
    print(cardSegments)
    print(crownSegments)

    # Multiplies the card array with the crown array, pluses the segment to the total result and prints it
    for i in range (len(cardSegments)):
        calculateSegment = cardSegments[i]*crownSegments[i]
        totalResult += calculateSegment
        if calculateSegment > 0:
            print(str(i)+". segment results in: "+str(calculateSegment)+ " points")
    print("Total points for board: "+str(totalResult))