import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def plot2DMaze(m, stackSize, newWindow = True):
	"""
	This function is used to plot the 2D representation of the maze.

	Args:
	m: An instance of the Room class representing the maze.
	stackSize: A matrix that represents the size of the stack in the maze.
	newWindow (optional): A boolean value which when True creates a new window for the plot. Defaults to True.
	"""
	# Bring the stack into the same coordinate system as the maze and plot it
	s = np.flipud(np.rot90(np.squeeze(stackSize)))
	# Plot the maze walls
	mazeSize = m.dimensions
	a = 0.48
	plotOffsets = [[a, a, -a, a],[-a,-a,-a,a],[a,-a,a,a],[a,-a,-a,-a]]
	for x in range(mazeSize[0]):
		for y in range(mazeSize[1]):
			for direction in range(4):
				if m.walls[direction][x,y]:
					o = offsets[direction]
					xData = [x+o[0], x+o[1]]
					yData = [y+o[2], y+o[3]]
					if newWindow:
						wallPlot = plt.plot(xData, yData, 'k-')
					else:
						wallPlot.set_data(xData, yData)
	if newWindow:
		stackPlot = plt.imshow(s, interpolation='nearest', origin='lower')
		plt.show()
	else:
		stackPlot.set_data(s)
		plt.draw()

def renderWalls(m, passageSize, wallThickness):
	"""
	This function renders walls of the maze by defining space for each cell and corner pillars.

	Args:
	m: An instance of the Room class representing the maze.
	passageSize: An integer value representing the size of the passage in the maze.
	wallThickness: An integer value representing the thickness of the walls in the maze.
	"""
	gridSize = m.dimensions # for example, (51,51,10)
	cellSize = passageSize + wallThickness * 2
	cornerBlocks = [[cellSize-wallThickness, cellSize], [0, wallThickness]]
	spaceSize = [g * cellSize for g in gridSize]
	space = np.zeros(spaceSize, dtype=bool)

	# Prepare the 2^dim corner pillars
	cornerSelectors = []
	for corner in range(2**len(gridSize)):
		if len(gridSize) <= 8: # for 8 dimensions or less
			cornerID = np.uint8(corner)
		else: # I doubt that everything else will survive more than 8 dimensions, but just to be safe
			cornerID = np.uint128 # if you actually build a maze with more than 8 dimensions - WHY??? please mail me
		bitArray = np.unpackbits(cornerID)
		croppedBitArray = bitArray[-len(gridSize):]
		cornerSelector = [slice((cellSize - 1) * c, (cellSize - 1) * c + 1, None) for c in croppedBitArray]
		cornerSelectors.append(cornerSelector)

	# Prepare the border walls
	blockSelectors = []
	for direction in range(len(m.walls)):
		blockSelector = [slice(None)] * len(gridSize)
		blockSide = direction % 2
		cornerElements = cornerBlocks[blockSide]
		dimension = direction // 2
		blockSelector[dimension] = slice(cornerElements[0], cornerElements[1])
		blockSelectors.append(blockSelector)

	for gridIndex in range(np.prod(gridSize)):
		gridCoordinates = np.unravel_index(gridIndex, gridSize)
		wallCell = [m.walls[direction][gridCoordinates] for direction in range(len(m.walls))]
		spaceCell = np.zeros([cellSize] * len(gridSize), dtype=bool)

		# draw the border walls
		for direction, wallSide in enumerate(wallCell):
			if wallSide:
				blockSelector = blockSelectors[direction]
				spaceCell[blockSelector] = True

		#draw the 2^dim corner pillars
		for cornerSelector in cornerSelectors:
			spaceCell[cornerSelector] = True

		gridSelector = []
		for dim in range(len(gridSize)):
			stopCoordinate = (gridCoordinates[dim] + 1) * cellSize
			startCoordinate = gridCoordinates[dim] * cellSize
			gridSelector.append(slice(startCoordinate, stopCoordinate))
		space[gridSelector] = spaceCell
	return space

def saveToPNG(renderedMaze, outputPath):
	"""
	This function saves the rendered maze to a PNG file.

	Args:
	renderedMaze: A matrix representing the rendered maze.
	outputPath: A string representing the path to save the PNG file.
	"""
	imageFilename = '{}/maze-layer{:d}.png'
	if len(renderedMaze.shape) == 2:
		image = Image.fromarray(np.rot90(np.uint8(renderedMaze)*255))
		image.save(imageFilename.format(outputPath, 0))
	elif len(renderedMaze.shape) == 3:
		for layer in range(renderedMaze.shape[2]):
			layerData = np.squeeze(renderedMaze[:,:,layer]) * 255
			image = Image.fromarray(np.uint8(layerData))
			image.save(imageFilename.format(outputPath, layer))