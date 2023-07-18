import random
import numpy as np

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
	def __init__(self, dimensions):
		self.dimensions = dimensions
		self.cells = np.ones(dimensions, dtype=bool)
		self.walls = [np.ones(dimensions, dtype=bool) for d in range(2 * len(dimensions))]

	def __repr__(self):
		return 'Room grid with dimensions {}'.format(self.dimensions)

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
			error('The two walls aren''t adjacent!')

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
	dim : int
		The dimension.

	offset : int
		The offset (-1, 1).

	Returns
	-------
	int
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
	for direction in xrange(maxDim * 2):
		d = direction % 2
		offset = offsets[d]
		dim = direction / 2
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
	dim = direction / 2
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
	for i in xrange(len(offsetTable)):
		position = addLists(currentPosition, offsetTable[i])
		dim = i / 2
		if 0 <= position[dim] <= roomSize[dim] - 1:
			positions.append(tuple(position))
		else:
			positions.append(None)
	return positions