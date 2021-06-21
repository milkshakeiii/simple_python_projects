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
		#given info about state
		snake_head_x, snake_head_y, snake_body, food_x, food_y = state

		# discretized state elements
		adj_wall_x = adj_wall_y = food_dir_x = food_dir_y = 0
		adj_body_top = adj_body_bottom = adj_body_right = adj_body_left = 0

		# getting discretized state elements
		if snake_head_x == 40:
			adj_wall_x = 1
		elif snake_head_x == 480:
			adj_wall_x = 2

		if snake_head_y == 40:
			adj_wall_y = 1
		elif snake_head_y == 480:
			adj_wall_y = 2

		if food_x < snake_head_x:
			food_dir_x = 1
		elif food_x > snake_head_x:
			food_dir_x = 2

		if food_y < snake_head_y:
			food_dir_y = 1
		elif food_y > snake_head_y:
			food_dir_y = 2

		if (snake_head_x,snake_head_y-40) in snake_body:
			adj_body_top = 1
		if (snake_head_x, snake_head_y+40) in snake_body:
			adj_body_bottom = 1
		if (snake_head_x-40,snake_head_y) in snake_body:
			adj_body_left = 1
		if (snake_head_x+40,snake_head_y) in snake_body:
			adj_body_right = 1

		# assembling discretized state
		disc_state = (adj_wall_x,adj_wall_y,food_dir_x,food_dir_y,adj_body_top,adj_body_bottom,adj_body_left,adj_body_right)

		reward = -0.1 #default for just taking another step
		if self._train and (self.s is not None):
			if points > self.points:
				reward = 1
			if dead:
				reward = -1

			alpha = self.C/(self.C + self.N[self.s + (self.a,)])
			self.Q[self.s + (self.a,)] += alpha*(reward + self.gamma*max([self.Q[disc_state+(new_a,)] for new_a in self.actions]) - self.Q[self.s + (self.a,)])

		#Taking action
		if dead:
			next_action = 0
		else:
			if self._train:
				actions_and_f = [(self.f(self.Q[disc_state+(a,)],self.N[disc_state+(a,)]),a) for a in self.actions]
				next_action = max(actions_and_f)[1]
			else:
				next_action = max([(self.Q[disc_state+(a,)],a) for a in self.actions])[1]

			self.N[disc_state+(next_action,)] += 1

		#Update all vars
		self.s = disc_state
		self.a = next_action
		self.points = points

		if dead:
			self.reset()

		return next_action

	def f(self, u, n):
		if n < self.Ne:
			return 1

		return u
