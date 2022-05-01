import numpy.random
import pygame
import sys
import os
from Creature import Creature
from Food import Food
import numpy as np
from tqdm import tqdm

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window


class WindowApp:
    """
    Creates the pygame Window and draws it
    """

    def __init__(self, width: int, height: int, title: str):
        self.title = title
        self.screen_size = [width, height]
        self.PyGameWindow = pygame.display.set_mode(self.screen_size, 8)
        self.clock = pygame.time.Clock()
        self.running = True
        self.init_app()

        # Evoling Simple creatures part
        self.list_of_food = []  # The array placeholder for food
        self.list_of_Bobs = []  # The creatures are called bob

        self.Number_of_creatures = 50  # NUmber of bobs
        self.Number_of_food = 125  # Number of food

        self.input_nodes = 1  # number of input nodes
        self.hidden_nodes = 5  # number of hidden nodes
        self.output_nodes = 2  # number of output nodes

        self.mutate_rate = 0.002  # Mutation rate
        self.elitism = .80  # elitism (selection bias)
        self.mutation_counter = 0  # Counter for mutation

        self.font = pygame.font.SysFont('verdana', 12)

        self.WallBoarder_start = 50
        self.WallBoarder_width = width - 100
        self.WallBoarder_height = height - 100
        self.WallBoarder = pygame.Rect(self.WallBoarder_start, self.WallBoarder_start, self.WallBoarder_width,
                                       self.WallBoarder_height)

        self.spawn_area = [100, 700]
        self.start_time = pygame.time.get_ticks()  # Get the current time
        self.change_health_event = pygame.USEREVENT + 1
        self.bob_count_death = 0
        self.fitness = 0
        pygame.time.set_timer(self.change_health_event, 1000)  # Every second

    def init_app(self):  # Initialize the pygame window
        pygame.init()
        pygame.display.set_caption(self.title)
        self.PyGameWindow.fill((255, 255, 255))
        self.running = True
        print("Application started")

    def on_execute(self):  # Main Loop that runs the game
        # Everything that should be run once should be here
        self.spawn_entities()
        while 1:  # Everything that needs to be looped should be in here
            self.process_input()
            self.update()
            self.on_render()
            self.simulate_entities()
            self.mutate_entities()
            self.clock.tick(60)
            pygame.display.update()  # display.flip is also available

    def status_txt(self):
        orgs_sorted_fitness = sorted(self.list_of_Bobs, key=lambda x: x.fitness, reverse=True)
        orgs_sorted_age = sorted(self.list_of_Bobs, key=lambda x: x.age, reverse=True)

        self.fitness = str(int(orgs_sorted_fitness[0].fitness))
        fitness_text = self.font.render("BEST FITNESS : " + self.fitness, True, (0, 0, 0))

        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render("FPS : " + str(fps), True, (0, 0, 0))

        time_in_sec = str(int((pygame.time.get_ticks() - self.start_time) / 1000))
        time_text = self.font.render("TIME : " + time_in_sec + " SECONDS", True, (0, 0, 0))

        mutation_counter = str(int(self.mutation_counter))
        mutation_text = self.font.render("MUTATION : " + mutation_counter, True, (0, 0, 0))

        oldest_age = str(int(orgs_sorted_age[0].age))
        oldest_age_text = self.font.render("OLDEST AGE : " + oldest_age, True, (0, 0, 0))

        length_of_list = str(len(self.list_of_Bobs))
        length_of_list_text = self.font.render("SUM OF BOBS : " + length_of_list, True, (0, 0, 0))

        death_counter = str(int(self.bob_count_death))
        death_text = self.font.render("DEATH : " + death_counter, True, (0, 0, 0))

        self.PyGameWindow.blit(fps_text, (20, 25))
        self.PyGameWindow.blit(fitness_text, (75, 25))
        self.PyGameWindow.blit(time_text, (200, 25))
        self.PyGameWindow.blit(mutation_text, (350, 25))
        self.PyGameWindow.blit(oldest_age_text, (465, 25))
        self.PyGameWindow.blit(length_of_list_text, (575, 25))
        self.PyGameWindow.blit(death_text, (700, 25))

    def on_render(self):  # Render the game state
        self.PyGameWindow.fill((255, 255, 255))  # Fill the screen with white
        self.status_txt()
        pygame.draw.rect(self.PyGameWindow, (0, 0, 0), self.WallBoarder, 1)

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def update(self):  # Update game state
        pass

    def process_input(self):  # Processes the input from the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.on_cleanup()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Mouse Clicked")
                print(f'pos = {pos}')
            if event.type == self.change_health_event:
                for bob in self.list_of_Bobs:
                    bob.health -= 1.0  # 0.1 is the amount of health lost per second
                    # print(f'Bob health = {bob.health}')
                    if bob.health == 0:
                        self.list_of_Bobs.remove(bob)
                        print(f'Bob died')
                        self.bob_count_death += 1
                        # print(f'Bob count death = {self.bob_count_death}')

                    # print(f'Bob lost health')

    #### Creature and everything else starts here  ###

    def distance(self, x1, y1, x2, y2):
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def calc_heading(self, creature, food):
        d_x = food.xPos - creature.xPos
        d_y = food.yPos - creature.yPos
        theta_d = np.degrees(np.arctan2(d_y, d_x)) - creature.r
        if abs(theta_d) > 180:
            theta_d += 360
        return theta_d / 180

    def simulate_entities(self):
        for bob in self.list_of_Bobs:
            bob.draw_creature()
        for foods in self.list_of_food:
            foods.draw_food()

        # UPDATE FITNESS FUNCTION
        for foods in self.list_of_food:
            for bob in self.list_of_Bobs:
                food_creature_dist = self.distance(bob.xPos, bob.yPos, foods.xPos, foods.yPos)

                # UPDATE FITNESS FUNCTION
                if food_creature_dist <= 0.80:  # Radius of the creature
                    bob.fitness += foods.energy
                    # print(f'Bob fitness: {bob.fitness}')
                    foods.respawn()
                    bob.health += 5
                    # print(f'Bob health: {bob.health}')

                # RESET DISTANCE AND HEADING TO NEAREST FOOD SOURCE
                bob.d_food = 100
                bob.r_food = 0

        # CALCULATE HEADING TO NEAREST FOOD SOURCE
        for foods in self.list_of_food:
            for bob in self.list_of_Bobs:

                # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
                food_creature_dist = self.distance(bob.xPos, bob.yPos, foods.xPos, foods.yPos)

                # DETERMINE IF THIS IS THE CLOSEST FOOD PARTICLE
                if food_creature_dist < bob.d_food:
                    bob.d_food = food_creature_dist
                    bob.r_food = self.calc_heading(bob, foods)

        # # GET ORGANISM RESPONSE
        for bob in self.list_of_Bobs:
            bob.think()

        # UPDATE ORGANISMS POSITION AND VELOCITY
        for bob in self.list_of_Bobs:
            bob.update_r()
            bob.update_vel()
            bob.update_pos()

        # for new_bob in self.list_of_new_bobs:
        #     self.list_of_Bobs.append(new_bob)

        return self.list_of_Bobs

    def mutate_entities(self, ):

        orgs_sorted = sorted(self.list_of_Bobs, key=lambda x: x.fitness, reverse=True)

        # SELECTION (TRUNCATION SELECTION)
        canidates = range(0, len(orgs_sorted))
        # canidates = range(0, settings['pop_size']-1)
        random_index = np.random.choice(a=canidates, size=2, replace=False)
        # print(f'random_index = {random_index}')

        creature_bob_1 = orgs_sorted[0]
        creature_bob_2 = orgs_sorted[1]

        # CROSSOVER
        crossover_weight = np.random.random()
        wih_new = (crossover_weight * creature_bob_1.wih) + ((1 - crossover_weight) * creature_bob_2.wih)
        who_new = (crossover_weight * creature_bob_1.who) + ((1 - crossover_weight) * creature_bob_2.who)

        mutate = np.random.random()
        if mutate <= self.mutate_rate and int(self.fitness) > 3:
            self.mutation_counter += 1
            print(f'Mutation occurred with Mutate rate: {mutate}')
            print(f'{creature_bob_1.name} Fitness : {creature_bob_1.fitness}')
            print(f'{creature_bob_2.name} Fitness : {creature_bob_2.fitness}')


            # MUTATE WEIGHTS
            matrix_pick = np.random.randint(0, 2)
            # MUTATE: WIH WEIGHTS
            if matrix_pick == 0:
                index_row = np.random.randint(0, self.hidden_nodes)
                index_col = np.random.randint(0, self.input_nodes)
                wih_new[index_row][index_col] = wih_new[index_row][index_col] * np.random.uniform(0.9, 1.1)

            # MUTATE: WHO WEIGHTS
            if matrix_pick == 1:
                index_row = np.random.randint(0, self.output_nodes)
                index_col = np.random.randint(0, self.hidden_nodes)
                who_new[index_row][index_col] = who_new[index_row][index_col] * np.random.uniform(0.9, 1.1)

            self.list_of_Bobs.append(
                Creature(surface=self.PyGameWindow, screen_size=[100, 700], health=100,
                         name=f'Bob Mutated ID{self.mutation_counter}',
                         wih=wih_new, who=who_new))

    def spawn_entities(self):

        self.input_nodes = 1  # number of input nodes
        self.hidden_nodes = 5  # number of hidden nodes
        self.output_nodes = 2  # number of output nodes

        # Creatures / Also called Bobs NEURAL NET SETTINGS
        #     # inodes = 1  # number of input nodes
        #     # hnodes = 5  # number of hidden nodes
        #     # onodes = 2  # number of output nodes

        # --- POPULATE THE ENVIRONMENT WITH FOOD ---------------+
        for i in range(self.Number_of_food):
            self.list_of_food.append(Food(surface=self.PyGameWindow, colour=(0, 255, 0)))
        # --- POPULATE THE ENVIRONMENT WITH ORGANISMS ----------+
        for i in range(self.Number_of_creatures):
            wih_init = np.random.uniform(-1, 1, (self.hidden_nodes, self.input_nodes))  # mlp weights (input -> hidden)
            who_init = np.random.uniform(-1, 1,
                                         (self.output_nodes, self.hidden_nodes))  # mlp weights (hidden -> output)
            # print(f'wih_init: {wih_init}')
            # print(f'who_init: {who_init}')
            self.list_of_Bobs.append(
                Creature(surface=self.PyGameWindow, screen_size=[100, 700], health=10, name=f'Bob_ID : {i}',
                         wih=wih_init, who=who_init))
