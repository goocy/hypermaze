import numpy as np
import scipy.sparse

def removeWalls(oldPos, newPos, room):
    # Check if locations are actually adjacent
    positionOffset = [n - o for n,o in zip(newPos, oldPos)]
    distance = sum([abs(p) for p in positionOffset])

    if distance == 1:
        direction = convertOffset(positionOffset)
        newWalls = [w[newPos] for w in room.walls]
        newWalls[direction] = False
        room.setWalls(newWalls, newPos)

        positionOffset = [o - n for n,o in zip(newPos, oldPos)]
        direction = convertOffset(positionOffset)
        oldWalls = [w[oldPos] for w in room.walls]
        oldWalls[direction] = False
        room.setWalls(oldWalls, oldPos)
    else:
        print('Positions not adjacent!')

    return room

def createHoles(room, holeVolume, holeCount):
    # Create a sequence of hyperrectangles that fulfill the volume criterium
    roomSize = room.cells.shape
    maxDim = len(roomSize)
    singleVolume = holeVolume / holeCount
    while not holeVolume * 0.95 < totalVolume < holeVolume * 1.05:
        rectangles = []
        totalVolume = 0
        for holeID in range(holeCount):
            # Create a single hyperrectangle
            averageLength = singleVolume**(1./maxDim)
            deviation = averageLength * 0.3
            dimensions = np.round(np.random.normal(averageLength, deviation, maxDim))
            rectangles.append(dimensions)
            volume = np.prod(dimensions)
            totalVolume += volume

    # If volume constraints are fulfilled, continue carving out these holes out of the grid
    totalAttempts = 0
    totalSuccess = False
    while not totalSuccess and totalAttempts < 10000 * len(rectangles):
        totalAttempts += 1
        sucesses = []
        for rectangle in rectangles:
            overlap = True
            totalRectangleAttempts = 0
            while overlap and totalRectangleAttempts < 1000:
                totalRectangleAttempts += 1
                selectionRange = [[]] * maxDim
                # place a random rectangle within the grid
                for d in range(maxDim):
                    point = random.randint(1, roomSize[d] - rectangle[d] - 1)
                    selectionRange[d] = np.array(range(point, point + rectangle[d]))
                # see if it overlaps with any other rectangle
                holeSlice = room.cells[selectionRange]
                overlap = np.all(holeSlice)
            if not overlap:
                # Set the rectangle to empty space (=False)
                successes.append(1)
                room.cells[selectionRange] = False

        # Check if all rectangles were placed
        totalSuccess = sum(successes) == len(rectangles)

    # If it didn't work out, start over with a new layout
    if totalAttempts >= 10000*len(rectangles):
        print('Too many holes to place without overlap!')
    return room

def carvePassages(room, startPosition, flatness):
    roomSize = room.cells.shape
    stackSize = np.zeros(roomSize, dtype=bool)
    visitedCells = np.zeros(roomSize, dtype=bool)
    if any([s>g for s, g in zip(startPosition, roomSize)]):
        error('startPosition outside of room dimensions!')
    visitedCells[startPosition] = True
    currentPosition = startPosition
    h = (np.arctan(flatness)/np.pi)+0.5 # percentage of horizontal wall crossings, in the range of ]0 1[
    directionalWeight = [h, h, h, h, 1-h, 1-h] # this needs to be adapted for multidimensional grids
    stack = []
    while sum(visitedCells) < np.prod(visitedCells.shape):
        neighborPositions = lookupDirections(currentPosition, directions, visitedCells.shape)
        neighborsVisited = [vistedCells[n] for n in neighborPositions]

        # If the current cell has any neighbours which have not been visited yet
        freeNeighbors = [u == 0 for u in neighborsVisited]
        if any(freeNeighbors):
            # Choose randomly one of the unvisitedCells neighbours
            if sum(freeNeighbors) > 1:
                freeNeighborIndices = [i for i, x in enumerate(freeNeighbors) if x == True]

                selectedDirection = weightedRandom(directionalWeight)
            else:
                selectedDirection = freeNeighbors.index(True)

            newPosition = lookupDirections(currentPosition, selectedDirection, roomSize)
            # Push the current cell to the stack
            stack.append(newPosition)
            stackSize.append(len(stack))
            # Remove the walls between the old and the new cell
            room = removeWall(currentPosition, newPosition, room)
            # Make the chosen cell the current cell and mark it as visited
            currentPosition = tuple(newPosition)
            visitedCells[currentPosition] = True
        
        elif not len(stack) == 0:
            currentPosition = stack[-1]
            stack[-1] = []
            if stackSize[-1] == 0:
                stackSize[-1] = len(stack)
        else:
            # Start with a random point
            currentPosition = []
            for i in range(len(roomSize)):
                randomIndex = weightedRandom([1]*roomSize[i])
                currentPosition.append(randomIndex)
            visitedCells[currentPosition] = True