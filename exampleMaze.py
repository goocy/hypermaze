import maze.helpers
import maze.excavation
import maze.plotTools

# Generate a maze
roomSize = (13,25)
flatness = (0.5,-0.5)
room = maze.helpers.Room(roomSize)
print(room.dimensions)
#holeyRoom = maze.excavation.createHoles(room, sum(roomSize) * 0.05, 5) # 5 holes with a total volume of 5%
entrancePoint = (0,11)
print('Carving passages...')
exampleMaze, stackSize = maze.excavation.carvePassages(room, entrancePoint, flatness, exitWallSide = exitWallSide, livePlot=False)

# Render the maze to voxels
passageSize = 8
print('Rendering walls...')
renderedMaze = maze.plotTools.renderWalls(exampleMaze, passageSize, 1)

# Plot the rendered maze to PNG
print('Saving to PNG')
maze.plotTools.saveToPNG(renderedMaze, 'maze.png')