from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random
import maze

def createHoles(room, holeVolume, holeCount):
	# Create a sequence of hyperrectangles that fulfill the volume criterium
	roomSize = room.cells.shape
	maxDim = len(roomSize)
	totalVolume = 0
	while not holeVolume * 0.98 < totalVolume < holeVolume * 1.02:
		rectangles = []
		singleVolume = holeVolume / holeCount # can be randomized later
		totalVolume = 0
		for holeID in range(holeCount):
			# Create a single hyperrectangle
			dimensions = []
			roomRatios = [d / roomSize[0] for d in roomSize] # determine room length ratios relative to the first side
			firstHoleSide = (singleVolume / np.prod(roomRatios))**(1./maxDim)
			holeSides = [r * firstHoleSide for r in roomRatios]
			for d in range(maxDim):
				averageLength = holeSides[d]
				deviation = averageLength * 0.3
				randomLength = roomSize[d] + 1
				while randomLength > roomSize[d]:
					randomLength = int(np.round(np.random.normal(averageLength, deviation, 1)))
				#print('randomLength: {}'.format(randomLength))
				dimensions.append(randomLength)
			rectangles.append(dimensions)
			volume = np.prod(dimensions)
			totalVolume += volume
		#print('totalVolume: {}'.format(totalVolume))

	# If volume constraints are fulfilled, continue carving out these holes out of the grid
	totalAttempts = 0
	totalSuccess = False
	while not totalSuccess and totalAttempts < 10000 * len(rectangles):
		totalAttempts += 1
		print('Placing {} rectangles, attempt {}'.format(len(rectangles), totalAttempts))
		successes = 0
		for rectangleID, rectangle in enumerate(rectangles):
			sliceIsFilled = False
			totalRectangleAttempts = 0
			while not sliceIsFilled and totalRectangleAttempts < 1000:
				totalRectangleAttempts += 1
				selectionRange = [[]] * maxDim
				# place a random rectangle within the grid
				for d in range(maxDim):
					if roomSize[d] > 1:
						endPoint = roomSize[d] - rectangle[d] - 1
						point = random.randint(0, endPoint)
						selectionRange[d] = range(point, point + rectangle[d])
					else:
						selectionRange[d] = [0]
				# Build a list of n-dimensional indices
				selection = [[]] * maxDim
				for goalDimension in range(maxDim):
					multiplier = 1
					for currentDimension in range(maxDim):
						if currentDimension == goalDimension:
							selectedRange = selectionRange[currentDimension]
						else:
							multiplier *= len(selectionRange[currentDimension])
					selection[goalDimension] = np.array(selectedRange * multiplier)
				# Import the selected slice of the room
				holeSlice = room.cells[selection]
				# Check if empty cells (from previous holes) exist in the selected slice
				sliceIsFilled = np.all(holeSlice)
			if sliceIsFilled:
				# Continue with the excavation: set the rectangle to empty space
				successes += 1
				room.cells[selection] = False
				print('Success at placing rectangle {}'. format(rectangleID))
			else:
				print('Overlap detected at rectangle {}'.format(rectangleID))

		# Check if all rectangles were placed
		totalSuccess = successes == len(rectangles)
		# If it didn't work out, start over with a new layout

	if totalAttempts >= 10000*len(rectangles):
		print('Too many holes to place without overlap!')
	return room

def carvePassages(room, startPosition, flatness, exitWallSide = -1, livePlot=True):
	roomSize = room.cells.shape
	offsetTable = maze.generateConversionTable(roomSize)
	stackSize = np.zeros(roomSize, dtype=int)
	if any([s>g for s, g in zip(startPosition, roomSize)]):
		error('startPosition outside of room dimensions!')
	room.cells[startPosition] = True
	currentPosition = startPosition
	directionalWeight = [(np.arctan(f)/np.pi)+0.5 for f in flatness for _ in (0,1)]
	# directionalWeight indicates the chance of a straight wall without corners, in the range of ]0% to 100%[
	# The "flatness" variable accepts one value for every dimension, from -inf to +inf
	# Example flatness values and passage probabilities: -31: 1%, -6.3: 5%, -1.4: 20%, 0: 50%, 1.4: 80%, 6.3: 95%, 31: 99%
	# Example: a flatness of (5, 5, -2) creates long passages and plenty of corners in the first two dimensions ("left/right", "forwards/backwards"), with only the occasional passage into the third dimension ("up/down")
	# Probability values are corrected afterwards so that they sum up to 100%
	stack = []
	filledCount = np.sum(room.cells)
	newPlot = True

	# Continue until all cells are empty
	while filledCount > 0:

		# Determine all possible neighbor positions
		neighborPositions = maze.findNeighborPositions(currentPosition, roomSize, offsetTable)
		neighborsFilled = []
		neighborsFilledCount = 0
		for neighborPosition in neighborPositions:
			if neighborPosition is not None:
				n = room.cells[neighborPosition]
				if n:
					neighborsFilledCount += 1
				neighborsFilled.append(n)
			else:
				neighborsFilled.append(False)

		# If the current cell has any non-empty neighbour cells
		if neighborsFilledCount > 0:
			# Choose (randomly) one of the unvisited neighbours
			if neighborsFilledCount > 1:
				currentWeight = [d * f for d, f in zip(directionalWeight, neighborsFilled)]
				selectedDirection = maze.weightedRandom(currentWeight)
			else:
				selectedDirection = neighborsFilled.index(True)

			newPosition = maze.lookupDirection(currentPosition, selectedDirection, roomSize, offsetTable)
			# Push the current cell to the stack
			if newPosition[1] == 5:
				print ('Breakpoint')
			stack.append(currentPosition)
			# Stack size is a simple indicator for "distance to the start point", so we save it for every point
			stackSize[currentPosition] = len(stack)
			# Remove the walls between the old and the new cell
			room.removeWalls(currentPosition, newPosition)
			# Make the chosen cell the current cell and mark it as empty
			currentPosition = tuple(newPosition)
			room.cells[currentPosition] = False
			filledCount -= 1
		
		elif not len(stack) == 0:
			# We're in a dead end, retrace our steps
			stackSize[currentPosition] = len(stack)
			currentPosition = stack.pop()
		else:
			# current position is in a dead end; start with different random point instead
			currentPosition = []
			for i in range(len(roomSize)):
				randomIndex = random.randint(0, roomSize[i])
				currentPosition.append(randomIndex)
			room.cells[currentPosition] = False
			filledCount -= 1

		# Plot the current maze if it's 2D
		a = 0.48
		plotOffsets = [[a, a, -a, a],[-a,-a,-a,a],[a,-a,a,a],[a,-a,-a,-a]] # No need to generalize; we can only plot in 2D anyways
		s = np.flipud(np.rot90(np.squeeze(stackSize)))
		if livePlot and len(roomSize) == 2:
			for x in range(roomSize[0]):
				for y in range(roomSize[1]):
					for direction in range(4):
						o = plotOffsets[direction]
						xData = [x+o[0], x+o[1]]
						yData = [y+o[2], y+o[3]]
						if newPlot:
							wallPlot = plt.plot(xData, yData, 'k-')
						else:
							wallPlot[0].set_data(xData, yData)
		if newPlot:
			stackPlot = plt.imshow(s, interpolation='nearest', origin='lower')
			newPlot = False
		else:
			stackPlot.set_data(s)
		plt.draw()
		plt.pause(0.2)


	# Create an exit at the appropriate side
	if exitWallSide == -1:
		exitWallSide = random.randint(0,5)
	# First, extract the correct wall from the array stackSize
	exitWallOffset = offsetTable[exitWallSide]
	exitWallDimension = exitWallSide // 2 # using the old Python 2 division on purpose
	exitWallIndex = sum(exitWallOffset)
	# Walls of an n-dimensional body are n-1-dimensional.
	# I'm constructing a selector that selects everything except for one dimension
	wallSelector = [slice(None)]*len(stackSize.shape) # slice takes up to three parameters: (start, stop, step). Passing None is equal to the [:] notation
	wallSelector[exitWallDimension] = slice(exitWallIndex, None, None) # this selects either the first, or the last element on this axis
	exitWall = stackSize[wallSelector]
	# Second, determine the coordinates of the largest element in the selected slice of stackSize
	# Selecting the biggest stackSize ensures that the exit is reasonably far away from the entrance
	exitWallElement = np.argmax(exitWall)
	exitCoordinates = list(np.unravel_index(exitWallElement, exitWall.shape))
	# Third, convert the local coordinates into global coordinates and remove the wall
	exitCoordinates[exitWallDimension] = exitWallIndex
	room.walls[exitWallSide][exitCoordinates] = False
	return room, stackSize, exitCoordinates