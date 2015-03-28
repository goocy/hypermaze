from __future__ import division
import numpy as np
import random
import maze

def removeWalls(oldPos, newPos, room):

    # Check if locations are actually adjacent
    dim, offset = maze.subtractLists(oldPos, newPos)

    if offset == 1 or offset == -1:
        direction = maze.convertOffset(dim, offset)
        room.walls[direction][newPos] = False

        dim, offset = maze.subtractLists(newPos, oldPos)
        direction = maze.convertOffset(dim, offset)
        room.walls[direction][oldPos] = False
    else:
        print('Positions not adjacent!')

    return room

def createHoles(room, holeVolume, holeCount):
    # Create a sequence of hyperrectangles that fulfill the volume criterium
    roomSize = room.cells.shape
    maxDim = len(roomSize)
    totalVolume = 0
    while not holeVolume * 0.98 < totalVolume < holeVolume * 1.02:
        rectangles = []
        singleVolume = holeVolume / holeCount # can be randomized later
        totalVolume = 0
        for holeID in range(holeCount):
            # Create a single hyperrectangle
            dimensions = []
            roomRatios = [d / roomSize[0] for d in roomSize] # determine room length ratios relative to the first side
            firstHoleSide = (singleVolume / np.prod(roomRatios))**(1./maxDim)
            holeSides = [r * firstHoleSide for r in roomRatios]
            for d in range(maxDim):
                averageLength = holeSides[d]
                deviation = averageLength * 0.3
                randomLength = roomSize[d] + 1
                while randomLength > roomSize[d]:
                    randomLength = int(np.round(np.random.normal(averageLength, deviation, 1)))
                #print('randomLength: {}'.format(randomLength))
                dimensions.append(randomLength)
            rectangles.append(dimensions)
            volume = np.prod(dimensions)
            totalVolume += volume
        #print('totalVolume: {}'.format(totalVolume))

    # If volume constraints are fulfilled, continue carving out these holes out of the grid
    totalAttempts = 0
    totalSuccess = False
    while not totalSuccess and totalAttempts < 10000 * len(rectangles):
        totalAttempts += 1
        print('Placing {} rectangles, attempt {}'.format(len(rectangles), totalAttempts))
        successes = 0
        for rectangleID, rectangle in enumerate(rectangles):
            sliceIsFilled = False
            totalRectangleAttempts = 0
            while not sliceIsFilled and totalRectangleAttempts < 1000:
                totalRectangleAttempts += 1
                selectionRange = [[]] * maxDim
                # place a random rectangle within the grid
                for d in range(maxDim):
                    if roomSize[d] > 1:
                        endPoint = roomSize[d] - rectangle[d] - 1
                        point = random.randint(0, endPoint)
                        selectionRange[d] = range(point, point + rectangle[d])
                    else:
                        selectionRange[d] = [0]
                # Build a list of n-dimensional indices
                selection = [[]] * maxDim
                for goalDimension in range(maxDim):
                    multiplier = 1
                    for currentDimension in range(maxDim):
                        if currentDimension == goalDimension:
                            selectedRange = selectionRange[currentDimension]
                        else:
                            multiplier *= len(selectionRange[currentDimension])
                    selection[goalDimension] = np.array(selectedRange * multiplier)
                # Import the selected slice of the room
                holeSlice = room.cells[selection]
                # Check if empty cells (from previous holes) exist in the selected slice
                sliceIsFilled = np.all(holeSlice)
            if sliceIsFilled:
                # Continue with the excavation: set the rectangle to empty space
                successes += 1
                room.cells[selection] = False
                print('Success at placing rectangle {}'. format(rectangleID))
            else:
                print('Overlap detected at rectangle {}'.format(rectangleID))

        # Check if all rectangles were placed
        totalSuccess = successes == len(rectangles)
        # If it didn't work out, start over with a new layout

    if totalAttempts >= 10000*len(rectangles):
        print('Too many holes to place without overlap!')
    return room

def carvePassages(room, startPosition, flatness):
    roomSize = room.cells.shape
    offsetTable = maze.generateConversionTable(roomSize)
    maxDim = len(roomSize)
    stackSize = np.zeros(roomSize)
    if any([s>g for s, g in zip(startPosition, roomSize)]):
        error('startPosition outside of room dimensions!')
    room.cells[startPosition] = True
    currentPosition = startPosition
    h = (np.arctan(flatness)/np.pi)+0.5 # percentage of horizontal wall crossings, in the range of ]0 1[
    directionalWeight = [h, h, h, h, 1-h, 1-h] # this needs to be adapted for multidimensional grids
    stack = []
    filledCount = np.sum(room.cells)
    # Continue until all cells are empty
    while filledCount > 0:
        # Determine all possible neighbor positions
        neighborPositions = maze.findNeighborPositions(currentPosition, roomSize, offsetTable)
        neighborsFilled = []
        neighborsFilledCount = 0
        for neighborPosition in neighborPositions:
            if neighborPosition is not None:
                n = room.cells[neighborPosition]
                if n:
                    neighborsFilledCount += 1
                neighborsFilled.append(n)
            else:
                neighborsFilled.append(False)

        # If the current cell has any non-empty neighbour cells
        if neighborsFilledCount > 0:
            # Choose randomly one of the unvisited neighbours
            if neighborsFilledCount > 1:
                currentWeight = [d * f for d, f in zip(directionalWeight, neighborsFilled)]
                selectedDirection = maze.weightedRandom(currentWeight)
            else:
                selectedDirection = neighborsFilled.index(True)

            newPosition = maze.lookupDirection(currentPosition, selectedDirection, roomSize, offsetTable)
            # Push the current cell to the stack
            stack.append(currentPosition)
            # Stack size is a simple indicator for "distance to the start point", so we save it for every point
            stackSize[currentPosition] = len(stack)
            # Remove the walls between the old and the new cell
            room = maze.removeWalls(currentPosition, newPosition, room)
            # Make the chosen cell the current cell and mark it as empty
            currentPosition = tuple(newPosition)
            room.cells[currentPosition] = False
            filledCount -= 1
        
        elif not len(stack) == 0:
            # We're in a dead end, retrace our steps
            stackSize[currentPosition] = len(stack)
            currentPosition = stack.pop()
        else:
            # current position is in a dead end; start with different random point instead
            currentPosition = []
            for i in range(len(roomSize)):
                randomIndex = maze.weightedRandom([1]*roomSize[i])
                currentPosition.append(randomIndex)
            room.cells[currentPosition] = False
            filledCount -= 1
    return room, stackSize