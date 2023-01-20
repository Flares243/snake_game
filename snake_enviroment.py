import pygame
import const
import numpy as np
import random
import math

pygame.init()
pygame.display.set_caption("Snake")

font = pygame.font.Font(None, 36)
food_color = pygame.Color(255, 0, 0)
snake_color = pygame.Color(255, 255, 255)
score_color = pygame.Color(255, 255, 255)
background_color = pygame.Color(0, 0, 0)

clock = pygame.time.Clock()

class SnakeEnviroment:
	def __init__(s):
		s.fps = 10
		s.game_speed = 2

		s.square_size = 40
		s.size = 10
		s.window_size = (
    	s.size * s.square_size,
     	s.size * s.square_size
    )

		s.screen = pygame.display.set_mode(s.window_size)

		s.initialize()
  
	def initialize(s):
		s.game_over = False
		s.score = 0
		s.snake = [
			[s.square_size * 5, s.square_size * 5],
			[s.square_size * 4, s.square_size * 5]
		]
		s.direction = const.RIGHT
		s.food_spawn = False
		s.spawn_food()
  
		return s.get_observation()
  
	def render(s):
		s.screen.fill(background_color)
    
		for snake_pos in s.snake:
			pygame.draw.rect(
				s.screen,
				snake_color,
				pygame.Rect(
      		snake_pos[0],
        	snake_pos[1],
         	s.square_size,
          s.square_size
        )
			)

		pygame.draw.rect(
			s.screen,
			food_color,
			pygame.Rect(
     		s.food_position[0],
       	s.food_position[1],
        s.square_size,
        s.square_size
      )
		)
  
		score_font = font.render("Score: " + str(s.score), True, score_color)
		s.screen.blit(score_font, (5, 10))

		pygame.display.update()

		clock.tick(s.fps * s.game_speed)

	def spawn_food(s):
		if not s.food_spawn:
			s.food_position = [
				random.randrange(0, s.window_size[0] - s.square_size, s.square_size),
				random.randrange(0, s.window_size[1] - s.square_size, s.square_size)
			]
   
			s.food_spawn = True

	def check_eat_food(s):
		if s.snake[0][0] == s.food_position[0] \
		and s.snake[0][1] == s.food_position[1]:
			s.food_spawn = False
			s.score += 1
		else:
			s.snake.pop()
   
	def check_game_over(s):
		if s.snake[0][0] < 0 or s.snake[0][0] > s.window_size[0] - s.square_size:
			s.game_over = True
		if s.snake[0][1] < 0 or s.snake[0][1] > s.window_size[1] - s.square_size:
			s.game_over = True
		else:
			for snake_body in s.snake[1:]:
				if s.snake[0][0] == snake_body[0] \
      	and s.snake[0][1] == snake_body[1]:
					s.game_over = True

	def update_snake_direction(s, action):
		if action == 0 and s.direction != const.DOWN:
			s.direction = const.UP
		elif action == 1 and s.direction != const.UP:
			s.direction = const.DOWN
		elif action == 2 and s.direction != const.RIGHT:
			s.direction = const.LEFT
		elif action == 3 and s.direction != const.LEFT:
			s.direction = const.RIGHT

	def move_snake(s):
		s.snake.insert(0, list(s.snake[0]))

		if s.direction == const.UP:
			s.snake[0][1] -= s.square_size
		elif s.direction == const.DOWN:
			s.snake[0][1] += s.square_size
		elif s.direction == const.LEFT:
			s.snake[0][0] -= s.square_size
		elif s.direction == const.RIGHT:
			s.snake[0][0] += s.square_size

	def get_observation(s):
		observation = np.zeros((
    	s.size + 2,
     	s.size + 2,
      3,
    ))
  
		# # Fill in wall observation
		observation[0, :, :] = [1, 0, 0]
		observation[-1, :, :] = [1, 0, 0]
		observation[:, 0, :] = [1, 0, 0]
		observation[:, -1, :] = [1, 0, 0]

		# Fill in food position
		x_food_shrink = (s.food_position[0] // s.square_size) + 1
		y_food_shrink = (s.food_position[1] // s.square_size) + 1

		# print(x_food_shrink)
		# print(y_food_shrink)
  
		observation[x_food_shrink, y_food_shrink] = [0, 1, 0]

		# Fill in snake position
		for x, y in s.snake:
			x_shrink = (x // s.square_size) + 1
			y_shrink = (y // s.square_size) + 1
   
			# print(x_shrink)
			# print(y_shrink)

			observation[x_shrink, y_shrink] = [0, 0, 1]

		return observation

	def get_reward(s):
		if s.game_over:
			return -1
		if not s.food_spawn:
			return 10
		return 0

	def step(s, action):
		s.update_snake_direction(action)

		# Must check_eat_food right after move_snake
		s.move_snake()
		s.check_eat_food()

		s.check_game_over()

		reward = s.get_reward()

		s.spawn_food()

		observation = s.get_observation()
  
		print(s.game_over)

		return observation, reward, s.game_over, {}