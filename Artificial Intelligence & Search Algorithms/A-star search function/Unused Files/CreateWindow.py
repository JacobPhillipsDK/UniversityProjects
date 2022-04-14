import pygame  # Import pygame module
import numpy as np
import math
from nodeClass import Node

# Colour options
background_colour = (255, 255, 255)  # White

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
# This sets the margin between each cell
MARGIN = 5
# The range of how many rows and columns that should be created
array_range = 10

global grid
global column
global row


def InitialiseWindowPyGame():
    # Initialize pygame
    pygame.init()

    # Pygame window settings
    WINDOW_SIZE = [255, 255]

    # Set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Path-A-star")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Set the screen background
    screen.fill(BLACK)

    done = False
    global grid
    grid = createGrid(screen)
    pygame.draw.rect(screen,
                     GREEN,
                     [(MARGIN + WIDTH) * 0 + MARGIN, (MARGIN + HEIGHT) * 0 + MARGIN, WIDTH, HEIGHT])

    pygame.draw.rect(screen,
                     RED,
                     [(MARGIN + WIDTH) * 9 + MARGIN, (MARGIN + HEIGHT) * 9 + MARGIN, WIDTH, HEIGHT])
    print("Hello I print ", grid[column - 1][row - 1])
    print(len(grid))
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                get_grid_value_from_mouse_click(grid)
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    pygame.quit()
    return None


def createGrid(pygame_screen):
    # Create a 2 dimensional array. A two-dimensional
    # array is simply a list of lists.
    global row
    global column
    grid = []
    for row in range(array_range):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(array_range):
            grid[row].append(0)  # Append a cell
            pygame.draw.rect(pygame_screen,
                             WHITE,
                             [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
    # Set row 1, cell 5 to one. (Remember rows and
    # column numbers start at zero.)
    return grid





def get_grid_value_from_mouse_click(grid):
    global column
    global row
    pos = pygame.mouse.get_pos()
    # Change the x/y screen coordinates to grid coordinates
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    # Set that location to one
    grid[row][column] = 1
    print("Click ", pos, "Grid coordinates: ", row, column)
    print(grid)
    return None


def draw_point_from_mouse(grid, game_screen):
    return None


def Euclidean_Distance_Heuristic(current_cell_x, current_cell_y, goal_cell_x, goal_cell_y):
    heuristic = math.sqrt((current_cell_x - goal_cell_x) ** 2 + (current_cell_y - goal_cell_y) ** 2)
    return heuristic


def a_star_algorithm(start_position, goal_position,heuristic):
    global grid
    print("Starting A-Star Algorithm")
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        Inspiration from : https://en.wikipedia.org/wiki/A*_search_algorithm
        :param grid:
        :param cost
        :param start_position:
        :param goal_position:
        :return:
        
    """
    Open_set= []  # The set of nodes to be evaluated
    Closed_set = []  # The set of nodes already evaluated


# def set_grid_value(grid, col, row, value):
#     grid[x][y] = value
#     return print(grid[x][y], value)


if "__main__" == __name__:
    InitialiseWindowPyGame()  # Initialise the window
    start_position = grid[0][0]
    end_position = grid[9][9]


    # path = a_star_algorithm(grid, cost, start_position, goal_position)  # Call the A* algorithm
    # print(path)
