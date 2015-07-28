import maze
import numpy as np
from matplotlib import pyplot as plt
roomSize = (51,51,1)
superMazeSize = (2,2,1)
flatness = (5,5,0)
room = maze.Room(roomSize)
# holeyRoom = maze.createHoles(room, sum(roomSize) * 0.05, 5) # 5 holes with a total volume of 5%
entrancePoint = (25,50,0)
exitWallSide = 1 # Left back wall or something
exampleMaze, exitPosition = maze.carvePassages(room, entrancePoint, flatness, exitWallSide = exitWallSide, livePlot=True)

#print m1