from PygameWindow import *


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Handles the PyGame and its creation
def create_PyGameWindow():
    evolving_creatures = WindowApp(width=800, height=800, title="Pygame Window")  # Create a new window
    evolving_creatures.on_execute()  # Execute the window and starts the game



if "__main__" == __name__:
    create_PyGameWindow()  # Create the pygame window
