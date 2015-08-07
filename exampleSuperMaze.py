import maze
import numpy as np
from matplotlib import pyplot as plt
superMazeSize = (2,2,1)
roomSize = (21,21,1)
flatness = (5,5,0)
for superMazeElement in superMaze.flat:
	room = maze.Room(roomSize)
	# holeyRoom = maze.createHoles(room, sum(roomSize) * 0.05, 5) # 5 holes with a total volume of 5%
	if entrancePoint is None:
		entrancePoint = (25,50,0)
	else:
		entrancePoint = exitPosition
	exitWallSide = ?
	segmentMaze, exitPosition = maze.carvePassages(room, entrancePoint, flatness, exitWallSide = exitWallSide, livePlot=True)

#print m1