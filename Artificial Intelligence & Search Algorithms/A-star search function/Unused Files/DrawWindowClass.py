BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class WindowPygame:
    def __init__(self, width: int, height: int, title: str, margin: int, screensize: (int, int)):
        import pygame
        self.pygame = pygame
        self.width = width
        self.height = height
        self.margin = margin
        self.pygame.init()
        self.screen = self.pygame.display.set_mode(screensize)
        self.pygame.display.set_caption(title)
        self.background = self.pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.clock = self.pygame.time.Clock()
        self.running = True
        self.grid = []
        self.colum = []
        self.row = []
        for row in range(10):
            self.grid.append([])
            for column in range(10):
                self.grid[row].append(0)  # Append a cell



    def run_window(self):
        while self.running:
            for event in self.pygame.event.get():  # User did something
                if event.type == self.pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == self.pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = self.pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (self.width + self.margin)
                    row = pos[1] // (self.height + self.margin)
                    # Set that location to one
                    self.grid[row][column] = 1
                    print("Click ", pos, "Grid coordinates: ", row, column)

            # Set the screen background
            self.background.fill(BLACK)

            # Draw the grid
            for row in range(10):
                for column in range(10):
                    color = WHITE
                    if self.grid[row][column] == 1:
                        color = GREEN
                    self.pygame.draw.rect(self.screen,
                                          color,
                                          [(self.margin + self.width) * column + self.margin,
                                           (self.margin + self.height) * row + self.margin,
                                           self.width,
                                           self.height])

    def create_grid(self):
        for row in range(len(self.grid)):
            self.grid.append([])
            for column in range(len(self.grid[row])):
                self.grid[row].append(0)  # Append a cell
        return self.grid


if __name__ == '__main__':
    screen = WindowPygame(width=20, height=20, title="A* Pathfinding Algorithm", margin=1, screensize=(600, 600))
    grid = screen.create_grid()
    print(grid)
