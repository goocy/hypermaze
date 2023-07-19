import numpy as np
import itertools
import random

"""
The class Room represents a room with certain dimensions, and methods for setting and removing walls at certain positions.
The weightedRandom() function chooses a random index from a list, with the probability of each index being chosen proportional to its corresponding weight.
The subtractLists() and addLists() functions perform element-wise subtraction and addition respectively on two lists.
The convertOffset() function converts a dimension and offset into an index used for wall placement and removal.
The generateConversionTable() function creates a conversion table that converts direction into a dimensional offset and vice versa.
The lookupDirection() function looks up the neighboring cell position given the current position and direction.
The findNeighborPositions() function finds all neighbor cell positions from the current position.
"""

class Room:
	"""
	A class with two main attributes: cells and walls.
	Both are initialized to be completely filled, so any maze will has to be excavated.
	cells is an n-dimensional array of booleans, where True represents filled space and False represents empty space.
	walls is a hyper-object. Each entry in the list is an n-dimensional array of booleans, where True represents a wall and False represents an opening.
		Each entry in this list represents a different direction in n-dimensional space.
		walls[0] and walls [1] represent the left and right walls respectively. walls[2] and walls[3] represent top and bottom walls, and this continues for higher dimensions.
	Only the walls variable is used for plotting the finished maze.
	"""
	def __init__(self, shape):
		self.shape = shape
		self.cells = np.ones(shape, dtype=bool)
		self.walls = [np.ones(shape, dtype=bool) for d in range(2 * len(shape))]

	def __repr__(self):
		return 'Room grid with dimensions {}'.format(self.shape)

	def setWalls(self, position, walls):
		"""
		Set the walls of a specific cell position in the room.

		Parameters
		----------
		position : tuple
			The position of the cell in the room.

		walls : list
			A list of walls to set at the specified position.
		"""
		if len(walls) == len(self.walls):
			for i, wall in enumerate(walls):
				self.walls[i][position] = wall

	def removeWalls(self, oldPos, newPos):
		"""
		Remove the walls between two adjacent cells.

		Parameters
		----------
		oldPos : tuple
			The position of the old cell.

		newPos : tuple
			The position of the new cell.
		"""
		offset = np.array(oldPos) - np.array(newPos)
		dim = np.where(offset)[0]
		if dim.size == 1:
			value = np.sum(offset)
			newDirection = convertOffset(dim[0], value)
			oldDirection = convertOffset(dim[0], -value)
			self.walls[newDirection][newPos] = False
			self.walls[oldDirection][oldPos] = False
		else:
			raise ValueError('The two walls aren''t adjacent!')

	def excavate_cavern(self, cavern):
		"""
		Excavate a cavern by setting all cells within the cavern to False and removing the walls within the cavern space.

		Parameters:
		cavern: dict
			A dictionary containing the position and shape of the cavern.
			The position is a tuple of coordinates indicating the starting corner of the cavern within the room.
			The shape is a tuple of dimensions indicating the size of the cavern to be excavated.

		"""
		position = np.array(cavern['position'])
		shape = np.array(cavern['shape'])

		# Establish the coordinate range of the cavern in each dimension
		coordinate_slices = [slice(p, p + d) for p, d in zip(position, shape)]

		# Set all cells in the room to False if they are within the cavern
		self.cells[tuple(coordinate_slices)] = False

		# For each cell in the cavern, remove the walls with its neighbors
		# We do this by iterating over all possible directions (i.e., neighboring cells) and call room.removeWalls() for each one.
		directions = [np.eye(len(shape), dtype=int), -np.eye(len(shape), dtype=int)]
		for direction in itertools.chain(*directions):

			# Get the slice in each dimension that has a neighbor in the current direction
			neighbor_slices = []
			neighbor_positions = []
			for p, d, s in zip(position, direction, self.shape):  # Iterate over each dimension of the room
				# Get the slice in the current dimension that has a neighbor in the current direction
				startPosition = max(p - d, 0)  # The start position of the slice is the current position minus the direction, but not less than 0
				endPosition = min(p + d, s - d)  # The end position of the slice is the current position plus the direction, but not more than the room size minus the direction
				neighbor_slice = slice(startPosition, endPosition)
				neighbor_slices.append(neighbor_slice)

				# Calculate the position of the neighbor in the current dimension
				neighbor_position = slice(np.clip(p + d, 0,
												  s - 1))  # The position of the neighbor is the current position plus the direction, but not less than 0 and not more than the room size minus 1
				neighbor_positions.append(neighbor_position)

			# Get all cells that have a neighbor in the current direction
			cells = np.array(np.where(self.cells[tuple(neighbor_slices)]))

			# For each cell, remove the wall with its neighbor in the current direction
			for cell in cells.T:
				self.removeWalls(tuple(cell), tuple(cell + direction))


def weightedRandom(weights):
	"""
	Returns a randomly selected element's index from the weights list,
	with higher weights increasing the probability of selection.

	Parameters
	----------
	weights : list
		A list of numerical weights.

	Returns
	-------
	int
		An index selected based on the weights.
	"""
	rnd = random.random() * sum(weights)
	for i, w in enumerate(weights):
		rnd -= w
		if rnd < 0:
			return i

def subtractLists(firstList, secondList):
	"""
	Subtracts the elements of the second list from the corresponding elements of the first list.

	Parameters
	----------
	firstList, secondList : list
		The two lists to be subtracted. They should have the same length.

	Returns
	-------
	list
		A list of element-wise differences between firstList and secondList.
	"""
	return [firstElement - secondElement for firstElement, secondElement in zip(firstList, secondList)]

def addLists(firstList, secondList):
	"""
	Adds together the elements of the two input lists.

	Parameters
	----------
	firstList, secondList : list
		The two lists to be added together. They should have the same length.

	Returns
	-------
	list
		A list of element-wise sums of firstList and secondList.
	"""
	return [firstElement + secondElement for firstElement, secondElement in zip(firstList, secondList)]

def convertOffset(dim, offset):
	"""
	Converts a dimension and offset into an index used for wall placement and removal.

	Parameters
	----------
	dim : ndarray
		The dimension.

	offset : ndarray
		The offset (-1, 1).

	Returns
	-------
	ndarray
		The converted index.
	"""
	# Convert [1, -1] to [0, 1]
	offsetIndex = [1, -1].index(offset)
	return dim * 2 + offsetIndex

def generateConversionTable(roomSize):
	"""
	Generates a conversion table that converts direction into a dimensional offset and vice versa.

	Parameters
	----------
	roomSize : list
		The dimensions of the room.

	Returns
	-------
	list
		A list of offset vectors representing the conversion table.
	"""
	# offsets come in the format [dim[0]+1, dim[0]-1, dim[1]+1, ...]
	maxDim = len(roomSize)
	offsetTable = list()
	offsets = [1, -1]
	for direction in range(maxDim * 2):
		d = direction % 2
		offset = offsets[d]
		dim = int(direction / 2)
		offsetVector = [0] * maxDim
		offsetVector[dim] = offset
		offsetTable.append(offsetVector)
	return offsetTable

def lookupDirection(currentPosition, direction, roomSize, offsetTable):
	"""
	Look up the neighboring cell position given the current position and direction.

	Parameters
	----------
	currentPosition : tuple
		The current position.

	direction : int
		The direction of movement.

	roomSize : list
		The dimensions of the room.

	offsetTable : list
		The conversion table from directions to offsets.

	Returns
	-------
	tuple
		The position of the neighbor cell. None if out of bounds.
	"""
	offsetVector = offsetTable[direction]
	neighborPosition = [o+c for o, c in zip(offsetVector, currentPosition)]
	dim = int(direction / 2)
	# Make an exception for grid boundaries
	if neighborPosition[dim] < 0 or neighborPosition[dim] > roomSize[dim] - 1:
		return None
	else:
		return tuple(neighborPosition)

def findNeighborPositions(currentPosition, roomSize, offsetTable):
	"""
	Find all neighbor cell positions from the current position.

	Parameters
	----------
	currentPosition : tuple
		The current position.

	roomSize : list
		The dimensions of the room.

	offsetTable : list
		The conversion table from directions to offsets.

	Returns
	-------
	list
		A list of positions for neighboring cells. None if out of bounds.
	"""
	positions = []
	for i in range(len(offsetTable)):
		position = addLists(currentPosition, offsetTable[i])
		dim = int(i / 2)
		if 0 <= position[dim] <= roomSize[dim] - 1:
			positions.append(tuple(position))
		else:
			positions.append(None)
	return positions