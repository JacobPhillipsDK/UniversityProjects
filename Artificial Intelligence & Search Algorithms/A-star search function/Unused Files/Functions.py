import pygame


def mouse_cords(grid, grid_width, grid_height, grid_margin, colour, screen, state):
    pos = pygame.mouse.get_pos()
    # Change the x/y screen coordinates to grid coordinates
    column = pos[0] // (grid_width + grid_margin)
    row = pos[1] // (grid_height + grid_margin)
    if row < len(grid) and column < len(grid[0]):
        print("Click ", pos, "Grid coordinates: ", row, column)
        draw_rect_from_click(grid=grid, grid_width=grid_width, grid_height=grid_height, grid_margin=grid, row=row,
                             column=column, x=0, y=0, colour=colour, screen=screen)
        grid[row][column].wall = state
        # self.grid[self.row][self.column] = 1
    # print(row < len(self.grid), "Row Value :", row) # Used at debugger value : To know when user clicks outside
    return None


def draw_rect_from_click(grid, grid_width, grid_height, grid_margin, row, column, x, y, colour, screen):
    if row < len(grid) and column < len(grid[0]):  # Check if user clicks outside the grid
        # if self.grid[self.row][self.column] == 0:
        pygame.draw.rect(screen,
                         colour,
                         [(grid_margin + grid_width) * column + x + grid_margin,
                          (grid_margin + grid_height) * row + y + grid_margin,
                          grid_width,
                          grid_height],
                         0,
                         border_radius=3)
        pygame.draw.rect(screen,
                         colour,
                         [(grid_margin + grid_width) * column + x + grid_margin,
                          (grid_margin + grid_height) * row + y + grid_margin,
                          grid_width,
                          grid_height],
                         2,
                         border_radius=3)
        print("Index Value : ", grid[row][column])
        # self.grid[self.row][self.column].wall = True
    return None
