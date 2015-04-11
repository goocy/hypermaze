import matplotlib.pyplot as plt
import numpy as np

def plot2DMaze(m, stack):
    s = np.flipud(np.rot90(stack.squeeze()))
    plt.imshow(s, interpolation='nearest', origin='lower')
    mazeSize = m.dimensions
    for x in range(mazeSize[0]):
        for y in range(mazeSize[1]):
            if m.walls[0][x,y,0]:
                plt.plot([x+0.5, x+0.5], [y-0.5, y+0.5], 'k-')
            if m.walls[1][x,y,0]:
                plt.plot([x-0.5, x-0.5], [y-0.5, y+0.5], 'k-')
            if m.walls[2][x,y,0]:
                plt.plot([x+0.5, x-0.5], [y+0.5, y+0.5], 'k-')
            if m.walls[3][x,y,0]:
                plt.plot([x+0.5, x-0.5], [y-0.5, y-0.5], 'k-')
    plt.show()