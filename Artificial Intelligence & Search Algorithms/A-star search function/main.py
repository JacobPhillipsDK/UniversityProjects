from PygameWindow import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# This sets the self.grid_width and HEIGHT of each grid location
WIDTH = 32
HEIGHT = 32
# This sets the margin between each cell
MARGIN = 2

x = 0  # x-coordinate of the top left corner of the grid
y = 0  # y-coordinate of the top left corner of the grid


def create_2d_array(rows: int, columns: int) -> [[]]:
    grid = [[0 for i in range(columns)] for j in range(rows)]
    return grid


def draw_grid(grid, screen):
    for row in range(len(grid)):
        for column in range(len(grid)):
            pygame.draw.rect(screen,
                             BLACK,
                             [(MARGIN + WIDTH) * column + x + MARGIN, (MARGIN + HEIGHT) * row + y + MARGIN, WIDTH,
                              HEIGHT],
                             2,
                             border_radius=3)


def create_PyGameWindow():
    grid = create_2d_array(rows=7, columns=7)  # Create grid based on row and colum value
    pygame_window = WindowApp(width=255, height=255, title="Pygame Window", bg_color=WHITE,
                              grid=grid, grid_width=WIDTH, grid_height=HEIGHT,
                              grid_margin=MARGIN, xPos=x, yPos=y)  # Create a new window
    screen = pygame_window.init_app(bg_color=pygame_window.bg_color)  # Initialize the pygame window

    start_position = pygame_window.set_start_position(grid, 0, 0)  # set the start position of the grid
    print(f'Start position: {start_position}')
    goal_position = pygame_window.set_goal_position(grid, 6, 6)  # set goal position
    print(f'Goal position: {goal_position}')

    draw_grid(grid, screen)  # Draw the grid
    pygame_window.run()  # run the pygame window


if "__main__" == __name__:
    create_PyGameWindow()  # Create the pygame window
