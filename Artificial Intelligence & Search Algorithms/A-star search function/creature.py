import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Creature:
    def __init__(self, velocity: int, size: int, node_grid_size: int, pygame_screen, grid_colour: tuple):
        self.x = 0
        self.y = 0
        self.x_change = 0
        self.y_change = 0
        self.velocity = velocity
        self.size = size
        self.node_grid_size = node_grid_size
        self.pygame_screen = pygame_screen
        self.grid_colour = grid_colour
        self.draw_creature()

    def draw_creature(self):
        head_rect = pygame.Rect(self.x, self.y, self.node_grid_size, self.node_grid_size)
        pygame.draw.rect(self.pygame_screen, self.grid_colour, head_rect)

    def move_creature_control(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y_change = -self.velocity
            self.x_change = 0
        if pressed_keys[K_DOWN]:
            self.y_change = self.velocity
            self.x_change = 0
        if pressed_keys[K_LEFT]:
            self.x_change = -self.velocity
            self.y_change = 0
        if pressed_keys[K_RIGHT]:
            self.x_change = self.velocity
            self.y_change = 0

        self.x += self.x_change
        self.y += self.y_change
