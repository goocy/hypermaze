import random
import numpy as np

class Room:
    def __init__(self, dimensions):
        dimensions = self.dimensions
        self.walls = 2 * len(dimensions) * [np.zeros(dimensions, dtype=bool),]
        self.cells = np.zeros(dimensions, dtype=bool)

    def __repr__(self):
        filled = np.sum(self.cells) / np.prod(dimensions)
        walled = np.sum(self.walls) / (np.prod(dimensions) * len(dimensions) * 2)
        return 'Room grid with dimensions {}x{}x{}, {:%} of all rooms filled, {:%} of all walls standing'.format(dimensions*, filled, walled)

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

def convertOffset(positionOffsetVector):
    # generate a direction integer from an n-dimensional offset (e.g., [0, -1, 0] -> 3)
    # Convert [1, -1] to [0, 1]
    positionOffset = sum(positionOffsetVector)
    o = [1, -1]
    offset = o.index(positionOffset)
    offsetDimension = positionOffsetVector.index(positionOffset)
    direction = offsetDimension * 2 + offset
    return direction

def convertDirection(direction):
    # Convert a direction integer into a dimension and a 
    # directions come in the format dim[0]+1, dim[0]-1, dim[1]+1, ...
    # example with two dimensions: x+1, x-1, y+1, y-1
    d = direction % 2
    o = [1, -1]
    offset = o[d]

    # Determine the position of the current neighbor
    dim = direction / 2 # this only works without proper division, but is so much faster
                        # otherwise use int(np.floor(direction/2))
    return dim, offset

def lookupDirections(currentPosition, directions, roomSize):
    positions = []
    for direction in directions: # Iterate through every possible dimensional direction
        # Initiate the offset for the current direction, e.g., -1
        dim, offset = convertDirection(direction)
        neighborPosition = list(currentPosition)
        neighborPosition[dim] += positionOffset

        # Make an exception for grid boundaries
        if neighborPosition < 0 or neighborPosition > roomSize[dim]:
            positions[direction] = None
        else:
            positions[direction] = neighborPosition
    return positions
