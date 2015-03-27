import maze
import numpy as np
from matplotlib import pyplot as plt
roomSize = (51,51,1)
room = maze.Room(roomSize)
#m = maze.createHoles(room, 250, 5)
m1, stackSize = maze.carvePassages(room, (25,50,0), 0.8)
plt.imshow(stackSize.squeeze(), interpolation='nearest')
plt.show()
print m1
# Hole with dimensions 1,2,3 at start point 5,6,7:
# x = 5,5,5,5,5,5
# y = 6,7,6,7,6,7
# z = 7,8,9,7,8,9