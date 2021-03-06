import random
import numpy as np

import pygame


class Creature:
    def __init__(self, surface: pygame.Surface, screen_size: [int, int], health: int, name: str, wih=None, who=None):

        ## Pygame Init part
        self.colour = (0, 0, 255)
        self.surface = surface  # The surface where it will de displayed/rendered
        self.xPos = random.uniform(screen_size[0], screen_size[1])  # Takes a random number from 0-screen-size
        self.yPos = random.uniform(screen_size[0], screen_size[1])  # Takes a random number from 0-screen-size

        self.limit_speed = 0.04
        self.dr_max = 720  # Max Rotational Speed
        self.v_max = 10  # Max Velocity
        self.dv_max = 15.0  # Max acceleration (+/-)

        self.r = random.uniform(0, 360)  # orientation   [0, 360] degrees
        self.v = random.uniform(0, self.v_max)  # velocity      [0, v_max]
        self.dv = random.uniform(-self.dv_max, self.dv_max)  # dv

        self.nn_dr = 0
        self.nn_dv = 0

        self.d_food = 100  # distance to the nearest food
        self.r_food = 0  # orientation to the nearest  food
        self.fitness = 0  # fitness (food count)
        self.radius = 10
        self.name = name

        # Weights Input Hidden
        self.wih = wih
        # Weight Hidden output
        self.who = who

        # self.age = 1  # age of the creature
        self.health = health  # health of the creature
        self.age = 0  # age of the creature

        self.debug_mode = False

        # NEURAL NETWORK

    def think(self):
        if self.health > 100:
            self.health = 100
        self.age += 0.005

        # SIMPLE MLP : Multilayer perceptron
        def af(input): # activation function
            return np.tanh(input)

        h1 = af(np.dot(self.wih, self.r_food))  # hidden layer
        out = af(np.dot(self.who, h1))  # output layer

        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_dv = float(out[0])  # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_dr = float(out[1])  # [-1, 1]  (left=1, right=-1)
        # nn_dv means the acceleration
        # nn_dr means the rotation

     # UPDATE HEADING
    def update_r(self): # [0, 360] degrees Rotations
        self.r += self.nn_dr * self.dr_max * self.limit_speed
        self.r = self.r % 360
        if self.debug_mode:
            print(f'self.r {self.r}')

    # UPDATE VELOCITY
    def update_vel(self):
        self.v += self.nn_dv * self.dv_max * self.limit_speed
        if self.v < 0:
            self.v = 0
        if self.v > self.v_max:
            self.v = self.v_max
        if self.debug_mode:
            print(f'Update vel : {self.v}')

     # UPDATE POSITION
    def update_pos(self):
        dx = self.v * np.cos(np.radians(self.r)) * self.limit_speed # x-axis
        dy = self.v * np.sin(np.radians(self.r)) * self.limit_speed # y-axis
        self.xPos += dx
        self.yPos += dy
        if self.debug_mode:
            print(f'Position update xPos : {self.xPos} yPos {self.yPos}')

    def draw_creature(self):
        pygame.draw.circle(surface=self.surface, color=self.colour, center=(self.xPos, self.yPos),
                           radius=self.radius, width=0).move(self.xPos, self.yPos)


        # Show food distance radius based on circle
        pygame.draw.circle(surface=self.surface, color=(255,0,0), center=(self.xPos, self.yPos),
                           radius=self.d_food, width=2).move(self.xPos, self.yPos)

        # # Draws the eye and nose of the creature
        # # The Nose
        pygame.draw.line(surface=self.surface, color=self.colour, start_pos=(self.xPos, self.yPos),
                         end_pos=(self.xPos, self.yPos - 15), width=3).move(self.xPos, self.yPos)
        pygame.draw.line(surface=self.surface, color=self.colour, start_pos=(self.xPos, self.yPos),
                         end_pos=(self.xPos, self.yPos + 15), width=3).move(self.xPos, self.yPos)
        #
        # # Eye Small evil eye
        pygame.draw.circle(surface=self.surface, color=(255, 255, 255), center=(self.xPos, self.yPos),
                           radius=7, width=0).move(self.xPos, self.yPos)
        pygame.draw.circle(surface=self.surface, color=(0, 0, 255), center=(self.xPos, self.yPos),
                           radius=3, width=0).move(self.xPos, self.yPos)
