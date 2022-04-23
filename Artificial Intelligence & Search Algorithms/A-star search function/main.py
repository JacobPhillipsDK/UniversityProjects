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
    """
    :param size: the size of the 2d array
    the value will create a array with size*size
    """
    grid = [[0 for i in range(size)] for j in range(size)]
    print("size :", size * size)
    print(f'grid {len(grid)}')
    return grid


def create_PyGameWindow():
    grid = create_2d_array(size=23)  # Create grid based on row and colum value

    pygame_window = WindowApp(width=800, height=800, title="Pygame Window",
                              grid=grid, grid_width=WIDTH, grid_height=HEIGHT,
                              grid_margin=MARGIN, xPos=x, yPos=y)  # Create a new window

    pygame_window.start = pygame_window.set_start_position(0, 0)  # set the start position of the grid
    pygame_window.goal = pygame_window.set_goal_position(len(grid) - 1, len(grid) - 1)  # set goal position
    pygame_window.cost = 1  # set the cost of each step
    pygame_window.debug = True

    print(f'Start position: {pygame_window.start}', f'Goal position: {pygame_window.goal}')
    pygame_window.on_execute()


if "__main__" == __name__:
    create_PyGameWindow()  # Create the pygame window
