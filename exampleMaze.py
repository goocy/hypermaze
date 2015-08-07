import maze

# Generate a maze
roomSize = (7,7)
flatness = (0,0)
room = maze.Room(roomSize)
# holeyRoom = maze.createHoles(room, sum(roomSize) * 0.05, 5) # 5 holes with a total volume of 5%
entrancePoint = (3,6)
exitWallSide = 1 # Left back wall or something
print('Carving passages...')
exampleMaze, stackSize, exitPosition = maze.carvePassages(room, entrancePoint, flatness, exitWallSide = exitWallSide, livePlot=True)

# Render the maze to voxels
passageSize = 2
print('Rendering walls...')
renderedMaze = maze.renderWalls(exampleMaze, passageSize, 1)

# Plot the rendered maze to PNG
print('Saving to PNG')
maze.saveToPNG(renderedMaze, '/Users/goocy/Downloads/Bukkit/maze')

# Insert the rendered maze into a Minecraft world
worldFilename = '/Users/goocy/Downloads/Bukkit/world/level.dat'
insertionHeight = 48
#print('Placing the maze...')
#mazeEntrance = maze.insertToMinecraft(worldFilename, renderedMaze, insertionHeight)
#print('Placed the maze entrance at coordinates X|{:d} Z|{:d} Y|{:d}'.format(*mazeEntrance))