import maze.helpers
import maze.plotTools
import maze.excavation

# Generate a maze
roomSize = (13,13)
flatness = (0.5,-0.5)
room = maze.helpers.Room(roomSize)
print(room.shape)
# holeyRoom = maze.excavation.carveCaverns(room, fillRatio=0.05, typicalCavernDiameter=5) # currently broken, don't use
entrancePoint = (0,11)
print('Carving passages...')
exampleMaze, stackSize = maze.excavation.carvePassages(holeyRoom, entrancePoint, flatness, livePlot=True)

# Render the maze to voxels
passageSize = 8
print('Rendering walls...')
renderedMaze = maze.plotTools.renderWalls(exampleMaze, passageSize, 1)

# Plot the rendered maze to PNG
print('Saving to PNG')
maze.plotTools.saveToPNG(renderedMaze, 'maze.png')