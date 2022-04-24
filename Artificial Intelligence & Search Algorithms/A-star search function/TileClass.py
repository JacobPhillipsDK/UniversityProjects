import pygame.image


class Tile:
    def __init__(self, tile_type: (int, int, int), tile_cost: int, grid_width, grid_height, grid_margin):
        self.tile_type = tile_type
        self.tile_cost = tile_cost

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_margin = grid_margin

    def draw_tile(self, row: int, column: int, border_radius, width, screen, x, y):
        pygame.draw.rect(screen,
                         self.tile_type,
                         [(self.grid_margin + self.grid_width) * column + x + self.grid_margin,
                          (self.grid_margin + self.grid_height) * row + y + self.grid_margin,
                          self.grid_width,
                          self.grid_height],
                         width,
                         border_radius=border_radius)

    def set_tile_grid_value(self, grid, row, column):
        grid[row][column] = self.tile_cost
