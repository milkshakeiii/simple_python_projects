import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        print (state[2])
        snake_head_x, snake_head_y, snake_body, food_x, food_y = state
        adjoining_wall_x = 0
        if snake_head_x == 40:
            adjoining_wall_x = 1
        if snake_head_x == 480:
            adjoining_wall_x = 2
        adjoining_wall_y = 0
        if snake_head_y == 40:
            adjoining_wall_y = 1
        if snake_head_y == 480:
            adjoining_wall_y = 2
        food_dir_x = 0
        if food_x < snake_head_x:
            food_dir_x = 1
        if food_x > snake_head_x:
            food_dir_x = 2
        food_dir_y = 0
        if food_y < snake_head_y:
            food_dir_y = 1
        if food_y > snake_head_y:
            food_dir_y = 2
        adjoining_body_top = adjoining_body_botom = adjoining_body_left = adjoining_body_right = 0
        if (snake_head_x + 0, snake_head_y - 1) in snake_body:
            adjoining_body_top = 1
        if (snake_head_x + 0, snake_head_y - 1) in snake_body:
            adjoining_body_bottom = 1
        if (snake_head_x + 0, snake_head_y - 1) in snake_body:
            adjoining_body_top = 1
        if (snake_head_x + 0, snake_head_y - 1) in snake_body:
            adjoining_body_top = 1
        
        
        state = [adjoining_wall_x,
                 adjoining_wall_y,
                 food_dir_x,
                 food_dir_y,
                 adjoining_body_top,
                 adjoining_body_bottom,
                 adjoining_body_left,
                 adjoining_body_right]
    
        def f(u, n):
            if n < self.Ne:
                return 1
            else:
                return u

        if not dead:
            if self._train:
                action = max([f(self.Q[state + [aprime]], self.N[state + [aprime]]) for aprime in self.actions])
            else:
                action = max([self.Q[state + [aprime]] for aprime in self.actions])
        else:
            self.reset()
            return 0

        if (self.s != None) and self._train:
            R = -0.1
            if dead:
                R = -1
            elif state[0] == state[3] and state[2] == state[4]:
                R = 1

            alpha = C / (C + self.N[self.s + [self.a]])
            self.Q[self.s + [self.a]] = self.Q[self.s + [self.a]] + alpha*(R + self.gamma*self.Q[state + [action]] - self.Q[self.s + [self.a]])

        self.s = state
        self.a = action
        return self.a
