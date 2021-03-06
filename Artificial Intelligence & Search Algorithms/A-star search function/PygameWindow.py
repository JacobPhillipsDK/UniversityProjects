from nodeClass import Node
import numpy as np
import pygame
import sys
import os
import random
from TileClass import Tile

os.environ['SDL_VIDEO_CENTERED'] = '1'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GRAY = (192, 192, 192)

# Tile Colours
# Dirt Tile
DIRT_TILE_COLOR = (64, 41, 5)
# Water Tile
WATER_TILE_COLOR = (0, 51, 102)
# Stone Tile
STONE_TILE_COLOR = (128, 128, 128)
# Forest Tile
FOREST_TILE_COLOR = (0, 128, 0)
# Sand Tile
SAND_TILE_COLOR = (193, 154, 107)


class WindowApp:
    """
    Creates the pygame Window and handles the drawing of the grid and the start and end positions
    """

    def __init__(self, width: int, height: int, title: str, grid: [[]], grid_width: int,
                 grid_height: int, grid_margin: int, xPos: int, yPos: int, DirtTileCost: int, WaterTileCost: int,
                 StoneTileCost: int, ForestTileCost: int, SandTileCost: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_margin = grid_margin
        self.screen_size = (width, height)

        self.grid = grid
        self.title = title
        self.x = xPos
        self.y = yPos

        self.total_cost = None

        self.PyGameWindow = pygame.display.set_mode(self.screen_size)

        self.clock = pygame.time.Clock()

        self.running = True
        self.run_a_star = False
        self.Diagonal = False

        self.row = None
        self.column = None
        self.goal = None
        self.start = None
        self.cost = 0
        self.debug = None
        self.draw_maze = True

        self.DirtTileCost = DirtTileCost
        self.WaterTileCost = WaterTileCost
        self.StoneTileCost = StoneTileCost
        self.ForestTileCost = ForestTileCost
        self.SandTileCost = SandTileCost
        self.all_sprites = pygame.sprite.Group()

        self.init_app()

    def init_app(self):  # Initialize the pygame window
        pygame.init()
        self.PyGameWindow.fill(WHITE)
        pygame.display.set_caption(self.title)
        self.running = True
        print("Application started")

    def check_values(self):
        if self.start is None:
            raise ValueError("Start, goal, and cost must be set to run the A* algorithm")

    def draw_grid(self):
        for row in range(len(self.grid)):
            for column in range(len(self.grid)):
                self.draw_rect(row=row, column=column, color=BLACK, border_radius=3, width=2)

    def draw_tiles(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                random_tile = random.randint(0, 4)
                if random_tile == 0:
                    Dirt_tile = Tile(tile_type=DIRT_TILE_COLOR, tile_cost=self.DirtTileCost, grid_width=self.grid_width,
                                     grid_height=self.grid_height, grid_margin=self.grid_margin)
                    Dirt_tile.draw_tile(row=i, column=j, border_radius=3, width=0, screen=self.PyGameWindow, x=0, y=0)
                    Dirt_tile.set_tile_grid_value(grid=self.grid, row=i, column=j)
                elif random_tile == 1:
                    Water_tile = Tile(tile_type=WATER_TILE_COLOR, tile_cost=self.WaterTileCost,
                                      grid_width=self.grid_width,
                                      grid_height=self.grid_height, grid_margin=self.grid_margin)
                    Water_tile.draw_tile(row=i, column=j, border_radius=3, width=0, screen=self.PyGameWindow, x=0, y=0)

                    Water_tile.set_tile_grid_value(grid=self.grid, row=i, column=j)
                elif random_tile == 2:
                    Sand_tile = Tile(tile_type=SAND_TILE_COLOR, tile_cost=self.SandTileCost, grid_width=self.grid_width,
                                     grid_height=self.grid_height, grid_margin=self.grid_margin)
                    Sand_tile.draw_tile(row=i, column=j, border_radius=3, width=0, screen=self.PyGameWindow, x=0, y=0)

                    Sand_tile.set_tile_grid_value(grid=self.grid, row=i, column=j)

                elif random_tile == 3:
                    Stone_tile = Tile(tile_type=STONE_TILE_COLOR, tile_cost=self.StoneTileCost,
                                      grid_width=self.grid_width,
                                      grid_height=self.grid_height, grid_margin=self.grid_margin)
                    Stone_tile.draw_tile(row=i, column=j, border_radius=3, width=0, screen=self.PyGameWindow, x=0,
                                         y=0)

                    Stone_tile.set_tile_grid_value(grid=self.grid, row=i, column=j)
                elif random_tile == 4:
                    Forest_tile = Tile(tile_type=FOREST_TILE_COLOR, tile_cost=self.ForestTileCost,
                                       grid_width=self.grid_width,
                                       grid_height=self.grid_height, grid_margin=self.grid_margin)
                    Forest_tile.draw_tile(row=i, column=j, border_radius=3, width=0, screen=self.PyGameWindow, x=0, y=0)

                    Forest_tile.set_tile_grid_value(grid=self.grid, row=i, column=j)

    def fix_mistakes(self):  # This function is used to fix mistakes in the grid
        self.draw_rect(row=0, column=0, color=GREEN, border_radius=3, width=0)
        self.draw_rect(row=0, column=0, color=BLACK, border_radius=3, width=2)

    def render_once(self):
        self.check_values()  # Check if the values are set
        self.draw_tiles()
        self.draw_grid()
        self.fix_mistakes()

    def on_execute(self):  # Main Loop that runs the game
        self.render_once()
        while self.running:
            self.process_input()
            self.update()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()

    def on_render(self):  # Render the game state
        # self.Alpha.move_creature(direction_x=1, direction_y=1)
        pygame.display.update()  # display.flip is also available

    def update(self):  # Update game state
        if self.run_a_star:
            self.run_a_star = False
            self.a_star_algorithm()

    def process_input(self):  # Processes the input from the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_cords()
                    self.draw_rect_from_click()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.goal is not None and self.start is not None:
                    self.run_a_star = True

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def a_star_algorithm(self):
        # inspiration : https://en.wikipedia.org/wiki/A*_search_algorithm

        start_position = Node(None, tuple(self.start))
        start_position.g = start_position.h = start_position.f = 0
        goal_position = Node(None, tuple(self.goal))
        goal_position.g = goal_position.h = goal_position.f = 0
        open_set = []  # Set of nodes to be evaluated, also called frontier
        closed_set = []  # Set of nodes already evaluated, also called reached

        open_set.append(start_position)

        # Movemment system - That can go in every direction
        if not self.Diagonal:
            move = [[-1, 0],  # go up
                    [0, -1],  # go left
                    [1, 0],  # go down
                    [0, 1]]  # go right
        else:  # Diagonal  movement system - That can go in 8 directions
            move = [[-1, 0],  # go up
                    [0, -1],  # go left
                    [1, 0],  # go down
                    [0, 1],  # go right
                    [-1, -1],  # go up left
                    [-1, 1],  # go up right
                    [1, -1],  # go down left
                    [1, 1]]  # go down right



        # find grid has got how many rows and columns
        row, column = np.shape(self.grid)

        print("Starting A* Algorithm")
        while len(open_set) > 0:  # While the length of the open_set list is longer than 0 do something
            current = open_set[0]  # Set current to the first element in the open_set list
            current_index = 0  # Set current_index to 0
            for index, item in enumerate(open_set):  # For each item in the open_set list
                if item.f < current.f:  # If the item's f value is less than the current's f value
                    current = item  # Set current to the item
                    current_index = index  # Set current_index to the index of the item
                    # if we hit this point return the path such as it may be no solution or
                    # computation cost is too high


                # Pop current node out off yet_to_visit list, add to visited list
            open_set.pop(current_index)
            closed_set.append(current)

            if current == goal_position:
                print("Found a path.")
                path = self.return_path(current)
                return path

            # Generate children from all adjacent squares
            children = []
            for new_position in move:
                # Get node position
                node_position = (current.position[0] + new_position[0], current.position[1] + new_position[1])
                # Create new node
                new_node = Node(current, node_position)
                # Append
                children.append(new_node)

                # Loop through children
            for child in children:

                arraychild = np.asarray(child.position)  # convert to array because im lazy

                if arraychild[0] == self.start[0] and arraychild[1] == self.start[
                    1]:  # Ensure the start position is not  overwritten with blue
                    self.draw_rect(row=arraychild[0], column=arraychild[1], color=GREEN, border_radius=3, width=0)
                    self.draw_rect(row=arraychild[0], column=arraychild[1], color=BLACK, border_radius=3, width=2)

                # Child is on the visited list (search entire visited list)
                if len([visited_child for visited_child in open_set if visited_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                current.cost = self.grid[current.position[0]][current.position[1]]
                #  gScore[neighbor] := tentative_gScore
                child.g = current.g + current.cost
                # Heuristic calculated Manhattan distance / Taxicab distance works better for grid than euclidean

                # tentative_gScore := gScore[current] + d(current, neighbor)
                child.h = self.Manhattan_distance(child.position, goal_position.position)

                # fScore[neighbor] := tentative_gScore + h(neighbor)
                child.f = child.g + child.h
                if len([i for i in open_set if child == i and child.g > i.g]) > 0:
                    continue
                # Add the child to the open_set list
                open_set.append(child)

    @staticmethod
    def Manhattan_distance(start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def return_path(self, current_node: Node):
        path = []  # List of nodes that make up the path

        current = current_node  # Current node is the goal node
        while current is not None:  #
            path.append(current.position)  # Add the current node to the path
            current = current.parent  # Set the current node to the parent of the current node

        path_to_draw = path[::-1]  # reverse the path to draw from start to end

        # Get total path cost
        get_path_cost = np.asarray(path_to_draw)  # Convert path to numpy array

        for i in range(len(get_path_cost)):
            self.cost = self.cost + self.grid[get_path_cost[i][0]][
                get_path_cost[i][1]]  # Add the cost of each node to the total cost
            # print(f' cost: {self.grid[get_path_cost[i][0]][get_path_cost[i][1]]}')

        print(f'path_to_draw: {path_to_draw}')

        path_to_draw.pop(0)  # remove the start position from the path to draw, so it is not overwritten
        path_to_draw.pop(-1)  # remove the end position from the path to draw, so it is not overwritten
        for i in range(len(path_to_draw)):
            for j in range(len(path_to_draw[i])):
                self.draw_rect(row=path_to_draw[i][0], column=path_to_draw[i][1], color=PURPLE, border_radius=3,
                               width=0)  # Draw the path rectangle
                # pygame.draw.rect(self.PyGameWindow,
                #                  PURPLE,
                #                  [(self.grid_margin + + self.grid_width) * path_to_draw[i][
                #                      1] + self.x + 5 + self.grid_margin,
                #                   (self.grid_margin + self.grid_height) * path_to_draw[i][
                #                       0] + self.y + 3 + self.grid_margin,
                #                   self.grid_width - 10,
                #                   self.grid_height - 10],
                #                  0,
                #                  border_radius=3)
                self.draw_rect(row=path_to_draw[i][0], column=path_to_draw[i][1], color=BLACK, border_radius=3,
                               width=2)  # Draw the path "outline"

        print(f'Total Cost: {self.cost}')  # Print the total cost of the path
        print('\n'.join([''.join(["{:" ">5d}".format(item) for item in row])
                         for row in self.grid]))  # Print the grid with values shown

        return path_to_draw

    def draw_rect(self, row: int, column: int, color: (int, int, int), border_radius, width):
        pygame.draw.rect(self.PyGameWindow,
                         color,
                         [(self.grid_margin + self.grid_width) * column + self.x + self.grid_margin,
                          (self.grid_margin + self.grid_height) * row + self.y + self.grid_margin,
                          self.grid_width,
                          self.grid_height],
                         width,
                         border_radius=border_radius)
        return

    def mouse_cords(self):
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        self.column = pos[0] // (self.grid_width + self.grid_margin)
        self.row = pos[1] // (self.grid_height + self.grid_margin)
        if self.row < len(self.grid) and self.column < len(self.grid[0]):
            print("Click ", pos, "Grid coordinates: ", (self.row, self.column))
            # self.grid[self.row][self.column] = 1
        # print(row < len(self.grid), "Row Value :", row) # Used at debugger value : To know when user clicks outside
        return None

    def draw_rect_from_click(self):
        if self.row < len(self.grid) and self.column < len(self.grid[0]):  # Check if user clicks outside the grid
            self.goal = (self.row, self.column)
            if self.debug:
                print(f'value of start: {self.goal}')
                print("Index Value : ", self.grid[self.row][self.column])
                print("Grid Value : ", self.grid[self.row][self.column])
            # self.grid[self.row][self.column] = 0
            self.draw_rect(row=self.row, column=self.column, color=RED, border_radius=3, width=0)
            self.draw_rect(row=self.row, column=self.column, color=BLACK, border_radius=3, width=2)
        return None

    def set_start_position(self, row: int, column: int) -> (int, int):
        self.draw_rect(row=row, column=column, color=GREEN, border_radius=3, width=0)
        self.draw_rect(row=row, column=column, color=BLACK, border_radius=3, width=2)
        position = (row, column)
        print(f'set_start_position : coordinates: [{row},{column}]')
        return position
