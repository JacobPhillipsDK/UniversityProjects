import pygame


class Creature:
    def __init__(self, colour: (int, int, int)):
        self.colour = colour

    def draw_creature(self, screen, x, y, pygame_screen: pygame.display):
        pygame_screen.draw.circle(screen, self.colour, (x, y), 5)
