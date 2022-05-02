from numpy.random import uniform
import pygame


class Food:
    def __init__(self, surface: pygame.surface, colour: (int, int, int)):
        self.colour = colour
        self.surface = surface
        self.xPos = uniform(100, 700)
        self.yPos = uniform(100, 700)
        # print(f' xPos : {self.xPos} yPos : {self.yPos}')
        self.energy = 1

    def respawn(self):
        self.xPos = uniform(100, 700)
        self.yPos = uniform(100, 700)
        self.energy = 1

    def draw_food(self):
        pygame.draw.circle(surface=self.surface, color=self.colour, center=(self.xPos, self.yPos),
                           radius=5, width=0)
