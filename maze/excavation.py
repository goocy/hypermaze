import matplotlib.pyplot as plt
import maze.helpers
import numpy as np
import random


def sample_random_value(typical_value, value_deviation):
	"""
	Generates a random sample based on a log-normal distribution.
	Log-normal distributions emulate distributions found in nature, such as the size of caves.

	Parameters:
	typical_value: float
		The desired median for a large sample of random values.

	value_deviation: float
		The variation in values.
		value_deviation = 0 means that all holes will be exactly typical_size.
		value_deviation = typical_value will make 5% of holes larger than 3 * typical_value and 5% smaller than typical_size / 3.
		value_deviation = typical_value * 5 will make 5% of holes larger than 20 * typical_value and 5% smaller than typical_size / 20.

	Returns:
	value: float
		A carefully randomized value. Ranges between 0 and infinity, with the median at typical_value.
	"""
	mu = np.log(typical_value)
	sigma = np.log1p(value_deviation / typical_value)
	value = np.random.lognormal(mu, sigma)
	return value


def cavern_diameter_to_shape(cavern_diameter, room_shape):
	"""
	Convert a cavern size and a room shape into a tuple of three cavern dimensions.

	Parameters:
	cavern_size: float
		The volume of the cavern.

	room_shape: tuple of int
		The shape of the room as a tuple of three integers (length, width, height).

	Returns:
	tuple of int
		The dimensions of the cavern as a tuple of three integers.
	"""
	# Calculate the typical length of a side of the cavern assuming it's a perfect cube
	cube_side_length = np.cbrt(cavern_diameter)

	# Calculate the room's aspect ratio
	room_aspect_ratio = np.array(room_shape) / np.min(room_shape)

	# Adjust the cavern's dimensions based on the room's aspect ratio
	cavern_shape = cube_side_length * room_aspect_ratio

	# Round the dimensions to the nearest integers and return as a tuple
	return tuple(np.round(cavern_shape).astype(int))


def find_cavern_position(room, cavernShape, maxAttempts=1000):
	"""
	Find a position in the room to place a new cavern.

	Parameters:
	room: object
		The room in which to place the cavern.
	cavernDimensions: tuple of int
		The dimensions of the cavern.
	maxAttempts: int, optional (default=1000)
		The maximum number of attempts to find a position.

	Returns:
	tuple of int or None
		The position of the cavern, or None if no position could be found after maxAttempts attempts.
	"""

	# check if the cavern would even fit into the room at all
	if any(cavernShape[i] > room.shape[i] for i in range(len(cavernShape))):
		return None

	for attempt in range(maxAttempts):

		# Randomly select a position within the room
		cavernPosition = tuple(np.random.randint(0, roomLength - cavernLength + 1) for roomLength, cavernLength in
							   zip(room.shape, cavernShape))

		# Check if the cavern would exceed any room boundaries
		if any(cavernPosition[i] + cavernShape[i] > room.shape[i] for i in range(len(cavernShape))):
			continue

		# Check if the cavern would overlap or touch any existing caverns
		# generate a slice of coordinates for the cavern, after adding a 1-cell buffer around the cavern
		cavernSlice = tuple(slice(cavernPosition[i] - 1, cavernPosition[i] + cavernShape[i] + 1) for i in range(len(cavernShape)))
		# apply the slice to the "cell" property of the room and ensure that all cells are True (so they're ready to be carved)
		if np.all(room.cells[cavernSlice]):
			# If the cavern fits and does not overlap or touch any existing cavern, return the position
			return cavernPosition

		# else: try again

	# If no position could be found after maxAttempts attempts, return None
	return None


def has_overlap_or_contact(position1, dimensions1, position2, dimensions2):
	"""
	Check if two rectangles defined by their position and dimensions overlap or contact each other.

	Parameters:
	position1, position2: tuple of int
		The positions of the rectangles.
	dimensions1, dimensions2: tuple of int
		The dimensions of the rectangles.

	Returns:
	bool
		True if the rectangles overlap or contact each other, False otherwise.
	"""
	for i in range(3):
		if position1[i] + dimensions1[i] + 1 <= position2[i] or position2[i] + dimensions2[i] + 1 <= position1[i]:
			return False
	return True


def carveCaverns(room, fillRatio, typicalCavernDiameter, sizeDeviation=1):
	"""
	Generate caverns in a given room. The cavern sizes will be drawn from a log-normal distribution, with a
	typical size and deviation determined by input parameters. The caverns will be carved in the room so as
	to roughly fill a target volume ratio.

	Parameters:
	room: ndarray
		A 3D numpy array representing the room. Caverns will be carved in this room.

	fillRatio: float
		The target ratio of the room's volume to be filled with caverns. Must be between 0 and 1.

	typicalCavernDiameter: float
		The diameter of the common cavern. Cavern sizes will be drawn from a log-normal random distribution.

	sizeDeviation: float
		The variation or deviation in cavern size. 0 means no variation, and 1 means that caverns can be as small as 1/3 of the typical size or as large as 3 times the typical size.

	Returns:
	room: ndarray
		The room after carving out the caverns.
	"""

	# Roughly estimate how many times we need to call the generate_cavern_size function
	roomVolume = np.prod(room.shape)
	targetCavernVolume = int(roomVolume * fillRatio)
	typicalCavernVolume = np.prod(cavern_diameter_to_shape(typicalCavernDiameter, room.shape))
	numberOfCaverns = int(targetCavernVolume / typicalCavernVolume)

	# Generate the estimated number of caverns and place it in the room, taking care to leave at least one wall of distance between caverns.
	# Cavern distribution throughout space is uniformly random.
	totalCavernVolume = 0
	caverns = []
	for i in range(numberOfCaverns):
		# Generate a cavern size
		cavernDiameter = sample_random_value(typicalCavernDiameter, sizeDeviation)
		cavernShape = cavern_diameter_to_shape(cavernDiameter, room.shape)
		cavernVolume = np.prod(cavernShape)

		# Update the total volume of the caverns
		totalCavernVolume += cavernVolume

		# If the total volume of the caverns exceeds the target volume
		if totalCavernVolume > targetCavernVolume:
			# Reduce the size of the last cavern to fit the remaining volume
			excessVolume = totalCavernVolume - targetCavernVolume
			cavernShape = cavern_diameter_to_shape(cavernDiameter - excessVolume, room.shape)
			totalCavernVolume = targetCavernVolume

		# Find a position for the cavern in the room
		cavernPosition = find_cavern_position(room, cavernShape)
		if cavernPosition is None:
			continue

		# Add the cavern to the list of caverns
		cavern = {'shape': cavernShape, 'position': cavernPosition}
		caverns.append(cavern)

		# Stop if the total volume of the caverns has reached the target volume
		if totalCavernVolume == targetCavernVolume:
			# Stop generating caverns
			break

		# Excavate the cavern by setting the cells to False and removing walls within cavern space
		room.excavate_cavern(cavern)

	return room


def getDirection(neighborsFilled, directionalWeights, lastSelectedDirections, staircasePattern=False):
	"""
	This function determines the direction in which the maze carving should proceed.

	Parameters
	----------
	neighborsFilled : list
		A list containing Boolean values indicating whether each neighbor cell around the current cell is filled or empty.

	directionalWeights : list
		A list of probabilities determining the chance of carving in each direction.

	lastSelectedDirections : list
		A list of the most recent directions selected, used to bias the carving in a particular direction.

	staircasePattern : bool
		A flag indicating whether to create a staircase pattern in the maze.

	Returns
	-------
	int
		The index of the selected direction in which to proceed with carving.
	"""

	# More fun pattern ideas:
	# Spiral Bias: Similar to the staircase, but with more of a rotation towards one direction, creating a more circular pattern.
	# Back and Forth Bias (or Zigzag): You could bias the directions to go back and forth along one axis, creating a series of parallel lines.
	# Random Direction Bias: While the maze carving is still fundamentally random, you could introduce biases towards randomly chosen directions at different points in the maze, creating a kind of patchwork of different directional biases.
	# Bias based on Distance to Center: The bias could be based on the distance to the center of the maze, creating patterns that radiate out from the middle.
	# Wave Bias: By taking into account the cell's coordinates, you can create biases that change over the grid, creating a sort of "wave" pattern in the final maze.

	if staircasePattern:
		# experimental attempt to generate staircase patterns
		if len(lastSelectedDirections) > 0:
			stairWeights = [0.1 for d in directionalWeights]
			lastDirection = lastSelectedDirections[0]
			if len(lastSelectedDirections) == 2:
				stairWeights[lastDirection] = 0.8
			elif len(lastSelectedDirections) == 1:
				stairWeights[lastDirection] = 0.3
				stairWeights[lastDirection - 1] = 0.8
				if lastDirection == len(stairWeights) - 1:
					lastDirection = -1
				stairWeights[lastDirection + 1] = 0.8
		else:
			stairWeights = [1 for d in directionalWeights]

		if neighborsFilled.count(True) > 1:
			validWeights = [d * f * s for d, f, s in zip(directionalWeights, neighborsFilled, stairWeights)]
			selectedDirection = maze.helpers.weightedRandom(validWeights)
		else:
			selectedDirection = neighborsFilled.index(True)
	else:
		# Choose (randomly) one of the unvisited neighbours
		if neighborsFilled.count(True) > 1:
			currentWeight = [d * f for d, f in zip(directionalWeights, neighborsFilled)]
			selectedDirection = maze.helpers.weightedRandom(currentWeight)
		else:
			selectedDirection = neighborsFilled.index(True)

	return selectedDirection


def carvePassages(room, startPosition, flatness, exitWallSide=-1, livePlot=True):
	"""
	This function generates a maze by carving passages in a given room based on specific rules and parameters.
	Documentation generated by ChatGPT4 on 2023-07-18

	Parameters
	----------
	room : object
		The object representing the room in which the maze is to be generated.
		The room object is expected to have a 'cells' attribute representing the grid of cells in the maze,
		and a 'removeWalls' method for removing walls between cells.

	startPosition : tuple
		The starting position for carving the maze, represented as coordinates in the room's grid.
		The function throws an error if the startPosition lies outside the room's dimensions.

	flatness : list or tuple
		Flatness indicates the probability of a straight wall without corners.
		The function accepts a flatness value for every dimension, from -inf to +inf.
		High positive flatness values create long passages with plenty of corners in the corresponding dimensions.

	exitWallSide : int, optional
		This parameter specifies the side of the maze where the exit will be created.
		If the value is -1 (default), the function will randomly choose a side to place the exit.
		Any value other than -1 is currently only implemented for 3D mazes:
		It is an integer from 0 to 5 where each integer represents a side of the 3D cube in the following manner: 0 -> left, 1 -> right, 2 -> bottom, 3 -> top, 4 -> front, 5 -> back.
		The function throws an error if the value lies outside the range -1 to 5.

	livePlot : bool, optional
		If True, the function will dynamically plot the current state of the maze after each step.
		Note that live plotting is only available for 2D mazes.
		Default value is True.

	Returns
	-------
	tuple
		Returns a tuple containing the final room object (with the maze carved in it) and a grid that stores the
		distance of each cell from the starting position.
	"""

	roomSize = room.shape
	offsetTable = maze.helpers.generateConversionTable(roomSize)
	stackSize = np.zeros(roomSize, dtype=int)
	if any([s > g for s, g in zip(startPosition, roomSize)]):
		raise ValueError("The starting position lies outside the room's dimensions.")
	room.cells[startPosition] = True
	currentPosition = startPosition
	directionalWeights = [(np.arctan(f) / np.pi) + 0.5 for f in flatness for _ in (0, 1)]
	# directionalWeights indicates the chance of a straight wall without corners, in the range of ]0% to 100%[
	# The "flatness" variable accepts one value for every dimension, from -inf to +inf
	# Example flatness values and passage probabilities: -31: 1%, -6.3: 5%, -1.4: 20%, 0: 50%, 1.4: 80%, 6.3: 95%, 31: 99%
	# Example: a flatness of (5, 5, -2) creates long passages and plenty of corners in the first two dimensions ("left/right", "forwards/backwards"), with only the occasional passage into the third dimension ("up/down")
	# Probability values are corrected afterwards so that they sum up to 100%
	stack = []
	lastSelectedDirections = []  # helper for the staircase idea
	filledCount = np.sum(room.cells)
	newPlot = True

	# Continue until all cells are empty
	while filledCount > 0:

		# Determine all possible neighbor positions
		neighborPositions = maze.helpers.findNeighborPositions(currentPosition, roomSize, offsetTable)
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
			selectedDirection = getDirection(neighborsFilled, directionalWeights, lastSelectedDirections)
			newPosition = maze.helpers.lookupDirection(currentPosition, selectedDirection, roomSize, offsetTable)
			# Push the current cell to the stack
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
			lastSelectedDirections = []  # helper for the staircase idea
		else:
			# current position is in a dead end; start with different random point instead
			currentPosition = []
			lastSelectedDirections = []
			for i in range(len(roomSize)):
				randomIndex = random.randint(0, roomSize[i])
				currentPosition.append(randomIndex)
			room.cells[currentPosition] = False
			filledCount -= 1

		# Plot the current maze if it's 2D
		a = 0.48
		plotOffsets = [[a, a, -a, a], [-a, -a, -a, a], [a, -a, a, a],
					   [a, -a, -a, -a]]  # No need to generalize; we can only plot in 2D anyways
		s = np.flipud(np.rot90(np.squeeze(stackSize)))
		if livePlot and len(roomSize) == 2:
			# first plot all the cells as squares: yellow for False, black for True
			for x in range(roomSize[0]):
				for y in range(roomSize[1]):
					if room.cells[x, y]:
						plt.plot(x, y, 'ko')
					else:
						plt.plot(x, y, 'yo')
			# then plot all the walls as lines: purple for True, white for False
			for x in range(roomSize[0]):
				for y in range(roomSize[1]):
					for direction in range(4):
						o = plotOffsets[direction]
						if room.walls[direction][x, y]:
							plt.plot([x + o[0], x + o[2]], [y + o[1], y + o[3]], 'm-')
						else:
							plt.plot([x + o[0], x + o[2]], [y + o[1], y + o[3]], 'w-')
		# finally, plot the stackSize array as a heatmap
		if newPlot:
			stackPlot = plt.imshow(s, interpolation='nearest', origin='lower')
			newPlot = False
		else:
			stackPlot.set_data(s)
		plt.draw()
		plt.pause(0.01)

	# Create an exit at the appropriate side
	if exitWallSide == -1:
		exitWallSide = random.randint(0, 5)
	# First, extract the correct wall from the array stackSize
	exitWallOffset = offsetTable[exitWallSide]
	exitWallDimension = exitWallSide // 2  # using the old Python 2 division on purpose
	exitWallIndex = sum(exitWallOffset)
	# Walls of an n-dimensional body are n-1-dimensional.
	# I'm constructing a selector that selects everything except for one dimension
	wallSelector = [slice(None)] * len(
		stackSize.shape)  # slice takes up to three parameters: (start, stop, step). Passing None is equal to the [:] notation
	wallSelector[exitWallDimension] = slice(exitWallIndex, None,
											None)  # this selects either the first, or the last element on this axis
	exitWall = stackSize[wallSelector]
	# Second, determine the coordinates of the largest element in the selected slice of stackSize
	# Selecting the biggest stackSize ensures that the exit is reasonably far away from the entrance
	exitWallElement = np.argmax(exitWall)
	exitCoordinates = list(np.unravel_index(exitWallElement, exitWall.shape))
	# Third, convert the local coordinates into global coordinates and remove the wall
	exitCoordinates[exitWallDimension] = exitWallIndex
	room.walls[exitWallSide][exitCoordinates] = False

	return room, stackSize, exitCoordinates
