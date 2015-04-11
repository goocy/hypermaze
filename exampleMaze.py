import maze
import numpy as np
import cProfile
from matplotlib import pyplot as plt
roomSize = (51,51,1)
room = maze.Room(roomSize)
#m = maze.createHoles(room, 250, 5)
entrancePoint = (25,50,0)
# cProfile.run('maze.carvePassages(room, entrancePoint, 0.8)')
m1, stack = maze.carvePassages(room, entrancePoint, 0.8)
maze.plot2DMaze(m1, stack)
#print m1