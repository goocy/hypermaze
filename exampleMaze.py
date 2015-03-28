import maze
import numpy as np
import cProfile
from matplotlib import pyplot as plt
roomSize = (501,501,1)
room = maze.Room(roomSize)
#m = maze.createHoles(room, 250, 5)
cProfile.run('maze.carvePassages(room, (250,500,0), 0.8)')
# m1, stackSize = maze.carvePassages(room, (50,100,0), 0.8)
#plt.imshow(stackSize.squeeze(), interpolation='nearest')
#plt.show()
#print m1
# Hole with dimensions 1,2,3 at start point 5,6,7:
# x = 5,5,5,5,5,5
# y = 6,7,6,7,6,7
# z = 7,8,9,7,8,9