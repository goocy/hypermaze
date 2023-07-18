import numpy as np
import maze.helpers
import maze.excavation

def mergeSuperMaze(superMaze, roomSize):
    """
    Merge the sections of a super maze into a single regular maze.

    This function takes a super maze, which is a high-level maze composed of smaller maze segments,
    and stitches these segments together into a single larger maze.

    Args:
        superMaze (np.ndarray): A multidimensional numpy array where each element is a maze object
            representing a segment of the super maze.
        roomSize (tuple): The size of each segment in the super maze, expressed as a tuple of integers.

    Returns:
        Room: A Room object representing the merged maze, with the cells and walls of each segment
            copied to the corresponding location in the merged maze.
    """
    # Calculate the total size of the merged maze
    mergedSize = tuple(s * r for s, r in zip(superMaze.shape, roomSize))

    # Create an empty room for the merged maze
    mergedMaze = maze.helpers.Room(mergedSize)

    # Iterate over each segment in the super maze
    for superMazeElement in np.ndindex(superMaze.shape):
        # Calculate the offset for this segment in the merged maze
        offset = tuple(s * r for s, r in zip(superMazeElement, roomSize))

        # Retrieve the segment maze
        segmentMaze = superMaze[superMazeElement]

        # Iterate over each cell in the segment maze
        for cell in np.ndindex(segmentMaze.dimensions):
            # Calculate the corresponding cell in the merged maze
            mergedCell = tuple(c + o for c, o in zip(cell, offset))

            # Copy the cell state and walls from the segment maze to the merged maze
            mergedMaze.cells[mergedCell] = segmentMaze.cells[cell]
            for i in range(len(segmentMaze.walls)):
                mergedMaze.walls[i][mergedCell] = segmentMaze.walls[i][cell]

    return mergedMaze

superMazeSize = (2,2,1)
roomSize = (21,21,1)
flatness = (5,5,0)

# Initialize a "super maze" to hold all of the individual segments
superMaze = np.empty(superMazeSize, dtype=object)

# Initialize entrancePoint
entrancePoint = (10,10,0)  # set entrance point to a position in the first room

# Iterate over each element of the super maze
for superMazeElement in np.ndindex(superMazeSize):
    room = maze.helpers.Room(roomSize)
    holeyRoom = maze.excavation.createHoles(room, sum(roomSize) * 0.05, 5)  # 5 holes with a total volume of 5%

    segmentMaze, exitPosition = maze.excavation.carvePassages(holeyRoom, entrancePoint, flatness, livePlot=True)

    # Store the segment maze in the super maze
    superMaze[superMazeElement] = segmentMaze

    # Set the entrance point for the next room to the exit position of the current room
    entrancePoint = exitPosition

# Merge the super maze into a regular maze
mergedMaze = mergeSuperMaze(superMaze, roomSize)