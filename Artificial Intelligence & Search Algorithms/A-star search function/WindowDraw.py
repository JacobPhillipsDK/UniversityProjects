import pygame


# Inspiration https://github.com/aspriya/gridai/blob/master/gridai.py


class DrawWindow:
    def __init__(self, pygame_screen_size: tuple, bg_colour: tuple, grid_colour: tuple, node_grid_size: int):
        self.grid_colour = grid_colour
        self.pygame_screen_size = pygame.display.set_mode(pygame_screen_size)
        self.pygame_screen_size.fill(bg_colour)
        self.node_grid_size = node_grid_size
        self.pygameInitialize()
        self.runtime()

    @staticmethod
    def pygameInitialize():
        pygame.init()  # initialize the pygame library
        pygame.display.set_caption("Path-Finding A* Search algorithm")  # Sets title for window
        clock = pygame.time.Clock()
        pygame.display.flip()
        pygame.display.update()  # update display

    @staticmethod
    def runtime():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



class DrawGrid(DrawWindow):
    def __init__(self):
        super().__init__(pygame_screen_size, bg_colour, grid_colour, node_grid_size)

