import pymclevel
import numpy as np
from scipy.ndimage.morphology import binary_erosion


def insertToMinecraft(worldFilename, renderedMaze, insertionHeight):
    """
    Inserts a rendered 3D maze into a specified Minecraft world at a given height.

    Parameters
    ----------
    worldFilename : str
        The filename (with the full path if needed) of the Minecraft world where the maze will be inserted.

    renderedMaze : ndarray
        A 3D numpy array representing the maze, where True values represent walls and False values represent passages.

    insertionHeight : int
        The y-coordinate in the Minecraft world where the bottom of the maze will be placed. This is the height in blocks
        above the bottom of the world. The world's height limit is 256 blocks, so the sum of insertionHeight and the height
        of the maze cannot exceed this value.

    Returns
    -------
    mazeEntrance : list
        A list containing the [x, z, y] coordinates of the entrance to the maze in the Minecraft world.

    Raises
    ------
    ValueError
        If the specified maze is too tall and exceeds the level limits by a certain number of blocks, or if the maze is
        too large to fit in the available area of the Minecraft world.

    Notes
    -----
    This function uses the pymclevel library to read and manipulate Minecraft world files. The maze is placed in such a
    way that it does not intersect with any existing structures in the world.
    """

    y = [insertionHeight, insertionHeight + renderedMaze.shape[2], renderedMaze.shape[2]]
    if y[1] > 256:
        error('Your maze is too tall and exceeds the level limits by {:d} blocks. Please lower insertionHeight or your maze.'.format(256 - y[1]))
    minecraftWorld = pymclevel.mclevel.fromFile(worldFilename)
    allChunkPositions = np.array(list(minecraftWorld.allChunks))
    # See if there are enough chunks to place the maze
    chunkMapSize = [-1,-1]
    chunkMapOrigin = [-1,-1]
    for dim in [0,1]:
        chunkMapSize[dim] = np.max(allChunkPositions[:,dim]) - np.min(allChunkPositions[:,dim]) + 1
        chunkMapOrigin[dim] = np.min(allChunkPositions[:,dim])
    chunkMap = np.zeros(chunkMapSize, dtype=bool)
    for chunkPosition in allChunkPositions:
        pos = [chunkPosition[dim] - chunkMapOrigin[dim] for dim in [0,1]]
        chunkMap[pos[0], pos[1]] = True
    mazeChunkSize = [int(np.ceil(renderedMaze.shape[dim] / 16)) for dim in [0,1]]
    halfMazeChunkSize = [int(np.ceil(mazeChunkSize[dim] / 2)) for dim in [0,1]]
    erodedWidthMap = binary_erosion(chunkMap, structure = np.ones((1,3)), iterations=mazeChunkSize[0])
    erodedHeightMap = binary_erosion(chunkMap, structure = np.ones((3,1)), iterations=mazeChunkSize[1])
    possiblePlacementMap = np.logical_and(erodedWidthMap, erodedHeightMap)
    if not possiblePlacementMap.any():
        errorText = 'Your maze is too big!\nTo insert this maze, generate an area of {:d}x{:d} blocks ({:d}x{:d} chunks)!'
        error(errorText.format(roomSize[0], roomSize[1], mazeChunkSize[0], mazeChunkSize[1]))
    possiblePlacementCoordinates = np.transpose(np.array(np.where(possiblePlacementMap)))
    distanceToZero = [(p[0] - chunkMapOrigin[0])**2 + (p[1] - chunkMapOrigin[1])**2 for p in possiblePlacementCoordinates]
    placementCenterCoordinates = possiblePlacementCoordinates[np.argmin(distanceToZero)]

    # Insert the maze into the Minecraft world
    airMaterial = minecraftWorld.materials.Air.ID
    wallMaterial = minecraftWorld.materials.BlockofIron.ID
    mazeOffset = [placementCenterCoordinates[dim] - halfMazeChunkSize[dim] + chunkMapOrigin[dim] for dim in [0,1]]
    for mazeXchunk in range(mazeChunkSize[0]):
        mazeXLims = [mazeXchunk*16, min((mazeXchunk+1)*16, renderedMaze.shape[0])]
        chunkXLims = mazeXLims[1] - mazeXLims[0]
        for mazeZchunk in range(mazeChunkSize[1]):
            mazeZLims = [mazeZchunk*16, min((mazeZchunk+1)*16, renderedMaze.shape[1])]
            chunkZLims = mazeZLims[1] - mazeZLims[0]
            wallSelector = renderedMaze[mazeXLims[0]:mazeXLims[1], mazeZLims[0]:mazeZLims[1], :]
            mazeChunk = np.ones((chunkXLims, chunkZLims, y[2])) * airMaterial
            mazeChunk[wallSelector] = wallMaterial
            chunk = minecraftWorld.getChunk(mazeXchunk + mazeOffset[0], mazeZchunk + mazeOffset[1])
            chunk.Blocks[:chunkXLims, :chunkZLims, y[0]:y[1]] = mazeChunk
            chunk.chunkChanged()
    mazeEntrance = [entrancePoint[dim] + mazeOffset[dim] for dim in [0,1]]
    mazeEntrance.append(entrancePoint[2] + insertionHeight)
    print('Recalculating lights...')
    minecraftWorld.generateLights()
    minecraftWorld.saveInPlace()
    return mazeEntrance