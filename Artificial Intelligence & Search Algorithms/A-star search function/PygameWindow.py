# Note to Jacob
# Grid value 1 will always mean start position
# Grid value 9 will always mean end position
#
import pygame


class WindowApp:
    """
    Creates the pygame Window and handles the drawing of the grid and the start and end positions
    """

    def __init__(self, width: int, height: int, title: str, bg_color: tuple[int, int, int], grid: [[]], grid_width: int,
                 grid_height: int, grid_margin: int, xPos: int, yPos: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_margin = grid_margin
        self.bg_color = bg_color
        self.screen_size = (width, height)
        self.grid = grid
        self.PyGameWindow = pygame.display.set_mode(self.screen_size)
        self.title = title
        self.running = True
        self.clock = pygame.time.Clock()
        self.row = 0
        self.column = 0
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.x = xPos
        self.y = yPos

    def init_app(self, bg_color: tuple[int, int, int]):
        pygame.init()
        self.PyGameWindow.fill(bg_color)
        pygame.display.set_caption(self.title)
        return self.PyGameWindow

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_cords()
                    self.draw_rect_from_click()
            pygame.display.flip()
            self.clock.tick(60)
        self.close_app()
        return None

    @staticmethod
    def close_app():
        pygame.quit()

    def mouse_cords(self):
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        self.column = pos[0] // (self.grid_width + self.grid_margin)
        self.row = pos[1] // (self.grid_height + self.grid_margin)
        if self.row < len(self.grid) and self.column < len(self.grid[0]):
            print("Click ", pos, "Grid coordinates: ", self.row, self.column)
            # self.grid[self.row][self.column] = 1
        # print(row < len(self.grid), "Row Value :", row) # Used at debugger value : To know when user clicks outside
        return None

    def draw_rect_from_click(self):
        if self.row < len(self.grid) and self.column < len(self.grid[0]):
            if self.grid[self.row][self.column] == 0:
                pygame.draw.rect(self.PyGameWindow,
                                 self.BLUE,
                                 [(self.grid_margin + self.grid_width) * self.column + self.x + self.grid_margin,
                                  (self.grid_margin + self.grid_height) * self.row + self.y + self.grid_margin,
                                  self.grid_width,
                                  self.grid_height],
                                 0,
                                 border_radius=3)
                self.grid[self.row][self.column] = 2
                print("Index Value : ", self.grid[self.row][self.column])
        return None

    def set_start_position(self, grid: [[]], row: int, column: int) -> [[]]:
        pygame.draw.rect(self.PyGameWindow,
                         self.GREEN,
                         [(self.grid_margin + self.grid_width) * column + self.x + self.grid_margin,
                          (self.grid_margin + self.grid_height) * row + self.y + self.grid_margin,
                          self.grid_width,
                          self.grid_height],
                         0,
                         border_radius=3)
        grid[row][column] = 1
        print(f'set_start_position : coordinates: [{row},{column}], value of Array.Index : {grid[row][column]}')
        return grid[row][column]

    def set_goal_position(self, grid: [[]], row: int, column: int) -> [[]]:
        pygame.draw.rect(self.PyGameWindow,
                         self.RED,
                         [(self.grid_margin + self.grid_width) * column + self.x + self.grid_margin,
                          (self.grid_margin + self.grid_height) * row + self.y + self.grid_margin,
                          self.grid_width,
                          self.grid_height],
                         0,
                         border_radius=3)
        grid[row][column] = 9
        print(f'set_goal_position : coordinates: [{row},{column}], value of Array.Index : {grid[row][column]}')
        return grid[row][column]
