import random
import numpy as np
import math

import pygame


class Food:
    def __init__(self, surface: pygame.surface, colour: (int, int, int)):
        self.colour = colour
        self.surface = surface
        self.xPos = random.uniform(0, 800)
        self.yPos = random.uniform(0, 800)
        # print(f' xPos : {self.xPos} yPos : {self.yPos}')
        self.energy = 1

    def respawn(self, screen_size: [int, int]):
        self.xPos = random.uniform(0, screen_size[1])
        self.yPos = random.uniform(0, screen_size[1])
        self.energy = 1

    def draw_food(self):
        pygame.draw.circle(surface=self.surface, color=self.colour, center=(self.xPos, self.yPos),
                           radius=5, width=0)

    def respawn_food(self):
        pass
