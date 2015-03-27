import numpy as np
import maze

def createMaze(dimensions, startPosition, passageProperties):
    # required input:
    # dimensions.room as [X Y Z]
    # dimensions.passage as [Width Height]
    # startPosition as [X Y Z]
    # roomVolume between 0 and 1 (0 introduces no empty rooms)
    # passageProperties.flatness between 0 and 1 (1 means mostly horizontal connections)
    # passageProperties.shortcutDensity between 0 and 1
    # passageProperties.shortcutStrength between 0 and 1 (0.2 allows shortcuts that shorten the way to exit by 20%)

    wallThickness = 1
    
    print('Creating empty grid of rooms')
    room = maze.Room(dimensions['room'])
    room = maze.createHoles(room)
    
    print('Carving passages')
    maze, stackSize = maze.carvePassages(room, startPosition, passageProperties['flatness'])
    print('Setting the exit point')
    maze, exitPoint = maze.createExit(maze, stackSize, startPosition)
    
    print('Clearing connected walls')
    maze = maze.excavation.clearConnectedWalls(maze, stackSize, passageProperties['shortcutDensity'], passageProperties['shortcutStrength'])
    #visualizeWalls(stackSize, maze)
    
    print('Rendering volume')
    renderedSpace = renderWalls(maze, dimensions['passage'], wallThickness)
    print('Merging intermediate passages')
    renderedSpace = mergeVerticalPassages(renderedSpace, dimensions, wallThickness)
    print('Cleaning leftover columns')
    renderedSpace = clearColumns(renderedSpace, wallThickness)
    print('Saving to PNG')
    saveToPNG(renderedSpace, './', 'medium')

dimensions = dict()
passageProperties = dict()
startPosition = (1,5,10)
dimensions['room'] = (10,10,10)
dimensions['passage'] = (3,3)
passageProperties['flatness'] = 0.2
passageProperties['shortcutDensity'] = 0.2
passageProperties['shortcutStrength'] = 0.2
createMaze(dimensions, startPosition, passageProperties)