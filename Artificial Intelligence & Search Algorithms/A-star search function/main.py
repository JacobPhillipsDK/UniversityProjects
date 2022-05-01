from PygameWindow import *
from nodeClass import Node

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# This sets the self.grid_width and HEIGHT of each grid location
WIDTH = 32
HEIGHT = 32
# This sets the margin between each cell
MARGIN = 2

# Used to move the whole grid left or right to down or up
x = 0  # x-coordinate of the top left corner of the grid
y = 0  # y-coordinate of the top left corner of the grid


def create_2d_array(size: int) -> [[]]:
    """Will return an array with size*size"""
    grid = [[0 for i in range(size)] for j in range(size)]
    return grid


def create_PyGameWindow():
    grid = create_2d_array(size=23)  # Create grid based on row and colum value

    DirtTileCost = 1
    WaterTileCost = 10
    SandTileCost = 5
    StoneTileCost = 7
    ForrestTileCost = 15

    PathAGame = WindowApp(width=800, height=800, title="Pygame Window",
                          grid=grid, grid_width=WIDTH, grid_height=HEIGHT,
                          grid_margin=MARGIN, xPos=x, yPos=y, DirtTileCost=DirtTileCost,
                          WaterTileCost=WaterTileCost, ForestTileCost=ForrestTileCost, SandTileCost=SandTileCost,
                          StoneTileCost=StoneTileCost)  # Create a new window

    PathAGame.start = PathAGame.set_start_position(0, 0)  # set the start position of the grid
    PathAGame.debug = False

    PathAGame.Diagonal = True

    PathAGame.on_execute()  # Execute the window and starts the game


if "__main__" == __name__:
    create_PyGameWindow()  # Create the pygame window
