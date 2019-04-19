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
        self.reset()

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
        ##compute TA's state rep
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
        #print ((food_x, food_y), (snake_head_x, snake_head_y), food_dir_x, food_dir_y)
        adjoining_body_top = adjoining_body_bottom = adjoining_body_left = adjoining_body_right = 0
        if (snake_head_x + 0, snake_head_y - 40) in snake_body:
            adjoining_body_top = 1
        if (snake_head_x + 0, snake_head_y + 40) in snake_body:
            adjoining_body_bottom = 1
        if (snake_head_x - 40, snake_head_y - 0) in snake_body:
            adjoining_body_left = 1
        if (snake_head_x + 40, snake_head_y - 0) in snake_body:
            adjoining_body_right = 1
        #print(snake_body, (snake_head_x, snake_head_y), adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right)
        
        state = (adjoining_wall_x,
                 adjoining_wall_y,
                 food_dir_x,
                 food_dir_y,
                 adjoining_body_top,
                 adjoining_body_bottom,
                 adjoining_body_left,
                 adjoining_body_right)

        #exploration function
        def f(u, n):
            return_value = None
            if n < self.Ne:
                return_value = 1
            else:
                return_value = u
            return return_value

        #update Q on all but the first turn
        if (self.s != None) and self._train:
            R = -0.1
            if dead:
                R = -1
            elif points > self.points:
                R = 1
                
            alpha = self.C / (self.C + self.N[self.s + (self.a,)])
            next_action_q = max([self.Q[state + (aprime,)] for aprime in self.actions])
            self.Q[self.s + (self.a,)] = self.Q[self.s + (self.a,)] + alpha*(R + self.gamma*next_action_q - self.Q[self.s + (self.a,)])

        #choose an action and update N if not dead
        if not dead:
            if self._train:
                possible_actions = [(f(self.Q[state + (aprime,)], self.N[state + (aprime,)]), aprime) for aprime in self.actions]
                action = max(possible_actions)[1]
                #print(possible_actions, action)
            else:
                action = max([(self.Q[state + (aprime,)], aprime) for aprime in self.actions])[1]

            self.N[state + (action,)] = self.N[state + (action,)] + 1
            
        else:
            action = 0

        self.points = points
        self.s = state
        self.a = action
        if dead:
            self.reset()
        return self.a
