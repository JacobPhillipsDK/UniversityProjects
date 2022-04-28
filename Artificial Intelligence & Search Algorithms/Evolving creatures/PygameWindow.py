import operator

import pygame
import sys
import os
from Creature import Creature
import random
from Food import Food
import numpy as np
import collections

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

        # Evoling Simple creatures part
        self.list_of_food = []  # The array placeholder for food
        self.list_of_Bobs = []  # The creatures are called bob
        self.Number_of_creatures = 25  # NUmber of bobs

        self.input_nodes = 1  # number of input nodes
        self.hidden_nodes = 5  # number of hidden nodes
        self.output_nodes = 2  # number of output nodes

        self.mutate = 0.10  # Mutation rate
        self.elitism = .20  # elitism (selection bias)
        self.generation_time = 100  # Generation length in seconds
        self.generation = 50  # number of generations
        self.plot = False

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
        for gen in range(0, self.generation):
            # Simulate part of the generation
            creature = self.simulate(foods=self.list_of_food, gen=self.generation, creatures=self.list_of_Bobs)
            # Evaluate the fitness of the creature
            creature, stats = self.evole(organisms_old=self.list_of_Bobs, gen=gen)
            print('> GEN:', gen, 'BEST:', stats['BEST'], 'AVG:', stats['AVG'], 'WORST:', stats['WORST'])
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
        # --- POPULATE THE ENVIRONMENT WITH FOOD ---------------+
        for i in range(30):
            self.list_of_food.append(Food(surface=self.PyGameWindow, colour=(255, 0, 0)))
        # --- POPULATE THE ENVIRONMENT WITH ORGANISMS ----------+
        for i in range(10):
            #     # ORGANISM NEURAL NET SETTINGS
            #     # inodes = 1  # number of input nodes
            #     # hnodes = 5  # number of hidden nodes
            #     # onodes = 2  # number of output nodes
            #
            wih_init = np.random.uniform(-1, 1, (5, 1))  # mlp weights (input -> hidden)
            who_init = np.random.uniform(-1, 1, (2, 5))  # mlp weights (hidden -> output)

            self.list_of_Bobs.append(Creature(surface=self.PyGameWindow, screen_size=self.screen_size,
                                              wih=wih_init, who=who_init,
                                              name=f'gen[x]-creature'))

        # for gen in range(0, self.generation):
        #     # Simulate part of the generation
        #     creature = self.simulate(foods=self.list_of_food, gen=self.generation, creatures=self.list_of_Bobs)
        #     # Evaluate the fitness of the creature
        #     creature, stats = self.evole(organisms_old=self.list_of_Bobs, gen=gen)
        #     print('> GEN:', gen, 'BEST:', stats['BEST'], 'AVG:', stats['AVG'], 'WORST:', stats['WORST'])

    def evole(self, organisms_old, gen):

        # settings['elitism'] = 0.20      # elitism (selection bias) = Hardcorded number of 0.20
        # settings['pop_size'] = 50       # number of organisms = self.Number_creatures

        elitism_num = int(np.floor(self.elitism * self.Number_of_creatures))
        new_orgs = self.Number_of_creatures - elitism_num

        # --- GET STATS FROM CURRENT GENERATION ----------------+
        stats = collections.defaultdict(int)
        for org in organisms_old:
            if org.fitness > stats['BEST'] or stats['BEST'] == 0:
                stats['BEST'] = org.fitness

            if org.fitness < stats['WORST'] or stats['WORST'] == 0:
                stats['WORST'] = org.fitness

            stats['SUM'] += org.fitness
            stats['COUNT'] += 1

        stats['AVG'] = stats['SUM'] / stats['COUNT']

        # --- ELITISM (KEEP BEST PERFORMING ORGANISMS) ---------+
        orgs_sorted = sorted(organisms_old, key=operator.attrgetter('fitness'), reverse=True)
        organisms_new = []
        for i in range(0, elitism_num):
            organisms_new.append(
                Creature(surface=self.PyGameWindow, screen_size=self.screen_size, wih=orgs_sorted[i].wih,
                         who=orgs_sorted[i].who,
                         name=orgs_sorted[i].name))

        # --- GENERATE NEW ORGANISMS ---------------------------+
        for w in range(0, new_orgs):

            # SELECTION (TRUNCATION SELECTION)
            canidates = range(0, elitism_num)
            random_index = random.sample(canidates, 2)
            org_1 = orgs_sorted[random_index[0]]
            org_2 = orgs_sorted[random_index[1]]

            # CROSSOVER
            crossover_weight = random.random()
            wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
            who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

            # MUTATION
            mutate = random.random()
            if mutate <= self.mutate:

                # PICK WHICH WEIGHT MATRIX TO MUTATE
                mat_pick = random.randint(0, 1)

                # self.input_nodes = 1  # number of input nodes
                # self.hidden_nodes = 5  # number of hidden nodes
                # self.output_nodes = 2  # number of output nodes

                # MUTATE: WIH WEIGHTS
                if mat_pick == 0:
                    index_row = random.randint(0, self.hidden_nodes - 1)
                    wih_new[index_row] = wih_new[index_row] * random.uniform(0.9, 1.1)
                    if wih_new[index_row] > 1:
                        wih_new[index_row] = 1
                    if wih_new[index_row] < -1:
                        wih_new[index_row] = -1

                # MUTATE: WHO WEIGHTS
                if mat_pick == 1:
                    index_row = random.randint(0, self.output_nodes - 1)
                    index_col = random.randint(0, self.hidden_nodes - 1)
                    who_new[index_row][index_col] = who_new[index_row][index_col] * random.uniform(0.9, 1.1)
                    if who_new[index_row][index_col] > 1:
                        who_new[index_row][index_col] = 1
                    if who_new[index_row][index_col] < -1:
                        who_new[index_row][index_col] = -1

            organisms_new.append(
                Creature(surface=self.PyGameWindow, screen_size=self.screen_size, wih=wih_new, who=who_new,
                         name='gen[' + str(gen) + ']-org[' + str(w) + ']'))

        return organisms_new, stats

    def distance(self, x1, y1, x2, y2):  # distance between two points
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calc_heading(self, creature, food):
        d_x = food.xPos - creature.xPos
        d_y = food.yPos - creature.yPos
        theta_d = np.degrees(np.arctan2(d_y, d_x)) - creature.r
        if abs(theta_d) > 180:
            theta_d += 360
        return theta_d / 180

    def simulate(self, foods, gen, creatures):

        #  total_time_steps = int(self.generation_time/dt) = total_time_steps = int(100/0.04)
        # dt is to Simulate time step used from the Creature class

        total_time_steps = int(self.generation_time / 0.04)

        # --- CYCLE THROUGH EACH TIME STEP ---------------------+
        for t_step in range(0, total_time_steps, 1):

            # PLOT SIMULATION FRAME

            # Plot final generation?
            for bob in self.list_of_Bobs:
                bob.move_creature()
            for food in self.list_of_food:
                food.draw_food()

            # UPDATE FITNESS FUNCTION
            for food in foods:
                for creature in creatures:
                    food_org_dist = self.distance(creature.xPos, creature.yPos, food.xPos, food.yPos)

                    # UPDATE FITNESS FUNCTION
                    if food_org_dist <= 0.075:
                        creature.fitness += food.energy
                        food.respawn()

                    # RESET DISTANCE AND HEADING TO NEAREST FOOD SOURCE
                    creature.d_food = 100
                    creature.r_food = 0

            # CALCULATE HEADING TO NEAREST FOOD SOURCE
            for food in foods:
                for creature in creatures:

                    # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
                    food_org_dist = self.distance(creature.xPos, creature.yPos, food.xPos, food.yPos)

                    # DETERMINE IF THIS IS THE CLOSEST FOOD PARTICLE
                    if food_org_dist < creature.d_food:
                        creature.d_food = food_org_dist
                        creature.r_food = self.calc_heading(creature, food)

            # GET ORGANISM RESPONSE
            for creature in creatures:
                creature.think()

            # UPDATE ORGANISMS POSITION AND VELOCITY
            for creature in creatures:
                creature.update_r()
                creature.update_vel()
                creature.update_pos()

        return creatures
