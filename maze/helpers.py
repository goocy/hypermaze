import random
import numpy as np

class Room:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.cells = np.ones(dimensions, dtype=bool)
        self.walls = [np.ones(dimensions, dtype=bool) for d in range(2 * len(dimensions))]

    def __repr__(self):
        return 'Room grid with dimensions {}'.format(self.dimensions)

    def setWalls(self, position, walls):
        if len(walls) == len(self.walls):
            for i, wall in enumerate(walls):
                self.walls[i][position] = wall

def weightedRandom(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

def subtractLists(firstList, secondList):
    for i in xrange(len(firstList)):
        if not firstList[i] == secondList[i]:
            return i, firstList[i] - secondList[i]

def addLists(firstList, secondList):
        result = []
        for listElement in xrange(len(firstList)):
            result.append(firstList[listElement] + secondList[listElement])
        return result

def convertOffset(dim, offset):
    # Convert [1, -1] to [0, 1]
    offsetIndex = [1, -1].index(offset)
    return dim * 2 + offsetIndex

def generateConversionTable(roomSize):
    # Convert a table that converts direction into a dimensional offset and vice versa
    # offsets come in the format [dim[0]+1, dim[0]-1, dim[1]+1, ...]
    # directions are a single number specifying the direction
    maxDim = len(roomSize)
    offsetTable = list()
    offsets = [1, -1]
    for direction in xrange(maxDim * 2):
        d = direction % 2
        offset = offsets[d]
        dim = direction / 2
        offsetVector = [0] * maxDim
        offsetVector[dim] = offset
        offsetTable.append(offsetVector)
    return offsetTable

def lookupDirection(currentPosition, direction, roomSize, offsetTable):
    offsetVector = offsetTable[direction]
    neighborPosition = [o+c for o, c in zip(offsetVector, currentPosition)]
    dim = direction / 2
    # Make an exception for grid boundaries
    if neighborPosition[dim] < 0 or neighborPosition[dim] > roomSize[dim] - 1:
        return None
    else:
        return tuple(neighborPosition)

def findNeighborPositions(currentPosition, roomSize, offsetTable):
    positions = []
    for i in xrange(len(offsetTable)):
        position = addLists(currentPosition, offsetTable[i])
        dim = i / 2
        if 0 <= position[dim] <= roomSize[dim] - 1:
            positions.append(tuple(position))
        else:
            positions.append(None)
    return positions
