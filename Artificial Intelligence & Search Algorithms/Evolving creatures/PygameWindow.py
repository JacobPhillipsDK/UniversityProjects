import pygame
import sys
import os
from Creature import Creature
import random
from Food import Food
import numpy as np

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window


class WindowApp:
    """
    Creates the pygame Window and draws it
    """

    def __init__(self, width: int, height: int, title: str):
        self.title = title
        self.screen_size = [width, height]
        self.PyGameWindow = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.init_app()

        self.list_of_food = []  # The array placeholder for food
        self.list_of_Bobs = []  # The creatures are called bob

    def init_app(self):  # Initialize the pygame window
        pygame.init()
        pygame.display.set_caption(self.title)
        self.PyGameWindow.fill((255, 255, 255))
        self.running = True
        print("Application started")

    def on_execute(self):  # Main Loop that runs the game
        # Everything that should be run once should be here
        self.spawn_entities()
        while self.running:  # Everything that needs to be looped should be in here
            self.process_input()
            self.on_render()
            self.update()
            self.clock.tick(60)

    def on_render(self):  # Render the game state
        pygame.display.update()  # display.flip is also available

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def update(self):  # Update game state
        self.PyGameWindow.fill((255, 255, 255))  # Refills the background colour for every frame
        for Bob in self.list_of_Bobs:
            Bob.think()
            Bob.update_r()
            Bob.update_vel()
            Bob.update_pos()
            Bob.move_creature()
        for food in self.list_of_food:
            food.draw_food()
        pass

    def process_input(self):  # Processes the input from the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.on_cleanup()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse Clicked")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Enter Pressed")

    #### Creature and everything else starts here  ###


    def spawn_entities(self):
        for i in range(30):
            self.list_of_food.append(Food(surface=self.PyGameWindow, colour=(255, 0, 0)))
        for i in range(15):
            #     # ORGANISM NEURAL NET SETTINGS
            #     # inodes = 1  # number of input nodes
            #     # hnodes = 5  # number of hidden nodes
            #     # onodes = 2  # number of output nodes
            #
            #     wih_init = np.random.uniform(-1, 1, (5, 1))  # mlp weights (input -> hidden)
            #     who_init = np.random.uniform(-1, 1, (2, 5))  # mlp weights (hidden -> output)

            self.list_of_Bobs.append(Creature(surface=self.PyGameWindow, screen_size=self.screen_size,
                                              wih=np.random.uniform(-1, 1, (5, 1)),
                                              who=np.random.uniform(-1, 1, (2, 5)),
                                              name=f'gen[x]-creature'))
