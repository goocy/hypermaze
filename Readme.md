# Hypermaze Generator

Hello there, interdimensional traveler! You found the perfect project for getting lost in the algorithmic labyrinths beyond the limitations of our earthly dimensions. This project allows you to generate mind-bending mazes of any number of dimensions, watch their creation in real-time, and save them for future exploration, research, or interdimensional fun.

## Overview

Typically, you would conjure a new fully-filled grid space from the Room class. Feel free to add caverns at this stage.
Then you etch passages between cells within the room, bringing the maze structures to life. You can watch the creation if you want, and of course there are numerous parameters to tune.

## Features

* **N-dimensional mazes**: Don't get restricted by the limits of our known reality! The core functions support as many dimensions as your computer can handle. Don't be ashamed if you start out with ordinary 2D mazes though, those can be fun too!

* **Flexible maze carving**: The excavation module allows you to specify the entrance point and the side of the exit wall. Whether you want a traditional one-way journey or an Escheresque maze that exits where it started, we've got you covered.

* **Hole carving**: Add tiny or huge caverns to your maze to make your minotaurs proud of their natural environment, and your travelers kneel in awe.  

* **Live Plotting**: Witness your maze getting born in real-time by setting the livePlot argument to True in the carvePassages function. It's like watching the birth of a universe, but with fewer physics involved.

* **Maze Rendering**: Our plotTools module will render your maze into beautiful voxels. You can even get lost inside your creation in Minecraft.

* **Save to PNG**: Once your maze has been lovingly carved and beautifully rendered, you can immortalize it as a PNG file to show off to your friends, or to perplex them with a challenge to find the exit.

## Using the Maze Generator

The following example will guide you through creating, carving, rendering, and saving a maze:

```python
import maze.helpers
import maze.excavation
import maze.plotTools

# Start as before
roomSize = (13,25)
room = maze.helpers.Room(roomSize)

# Add some holes to your maze
# You can specify the total volume of the holes and the maximum size of each hole
print('Creating holes...')
holeyRoom = maze.excavation.createHoles(room, sum(roomSize) * 0.05, 5)

# Continue with the process as before
entrancePoint = (0,11)
print('Carving passages...')
exampleMaze, stackSize = maze.excavation.carvePassages(holeyRoom, entrancePoint, flatness, livePlot=False)

print('Rendering walls...')
renderedMaze = maze.plotTools.renderWalls(exampleMaze, passageSize, 1)

print('Saving to PNG')
maze.plotTools.saveToPNG(renderedMaze, 'maze.png')

```

And there you have it! Your very own interdimensional maze.



# Core Functions

This section provides a quick rundown of how each function works and how you can use them to craft your perfect maze.

## Maze Helper Functions

### `Room()`

This function initializes a new Room object with specified dimensions. The Room class stores the layout of your maze, including the cells and walls.

### `setWalls()`

This method of the Room class allows you to define walls in a specific position of the room. The wall definitions are provided as a list of Booleans, with each Boolean value indicating whether a wall exists or not in the corresponding position.

### `removeWalls()`

This Room class method is used to remove walls between two adjacent cells, effectively creating a passage between them. The function ensures that the cells are indeed adjacent and that no diagonal passages are created.

## Maze Excavation Functions

### `createHoles()`

This function adds rooms to your maze. Rooms are a series of interconnected cells, making your maze less claustrophobic and more diverse. Rooms can serve as special points of interest in your maze, providing places to store unique items or setups. The total volume of rooms and the maximum size of each room can be specified.

### `carvePassages()`

This function is the main driver of the maze generation process. Starting from a specified entrance point, it uses a random walk algorithm to carve passages through your maze. The direction of carving is biased by a flatness factor, which controls how likely the function is to continue carving in the same direction.

The function also ensures that the maze is solvable by maintaining a stack of carved cells, and backtracking when it encounters a dead end. The function returns the finished maze and a stack indicating the order in which cells were carved.

## Maze Plot Tools Functions

### `renderWalls()`

This function renders the walls of your maze as voxels, based on the passage size and wall thickness you specify. It returns a 3D NumPy array where True indicates a wall and False indicates a passage.

### `saveToPNG()`

This function saves your rendered maze as a PNG image, which you can view or share. It supports both 2D and 3D mazes, and saves each layer of a 3D maze as a separate PNG file.

## Using the Core Functions

These functions are meant to be used in conjunction, allowing you to create, modify, render, and save your maze. The maze is initially created as a Room object, and then the maze excavation functions are used to carve passages and create rooms. The finished maze can then be rendered and saved as a PNG file using the plot tools functions. All of these steps can be modified or extended as needed, allowing you to craft the perfect maze to meet your needs.

## Conclusion

The labyrinth is an ancient symbol that transcends the limits of our physical reality. By creating your own hyper-dimensional maze, you're not just making a cool program, you're part of a grand, mysterious tradition. So go ahead, create your maze, make it weird, make it wonderful, and remember to enjoy the journey as much as the destination.

## License

This project is licensed under the terms of the MIT license.

Happy Hypermaze Making! 🚀🌌🌠
