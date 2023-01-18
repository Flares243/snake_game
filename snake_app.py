import const
import random
import pygame

pygame.init()
square_size = 20
window_size = (square_size * 26, square_size * 26)
screen = pygame.display.set_mode(window_size)
snake_head_position = [square_size * 5, square_size * 5]
snake_body = [
	[square_size * 4, square_size * 5],
]
direction = const.RIGHT
change_to = direction
food_position = [
	random.randrange(1, (window_size[0] // square_size)) * square_size,
	random.randrange(1, (window_size[1] // square_size)) * square_size
]
food_spawn = True
score = 0
game_over = False
pygame.display.set_caption("Snake")
font = pygame.font.Font(None, 36)
food_color = pygame.Color(255, 0, 0)
snake_color = pygame.Color(255, 255, 255)
score_color = pygame.Color(255, 255, 255)
background_color = pygame.Color(0, 0, 0)
fps = 10
game_speed = 1
clock = pygame.time.Clock()

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				change_to = const.UP
			if event.key == pygame.K_DOWN:
				change_to = const.DOWN
			if event.key == pygame.K_LEFT:
				change_to = const.LEFT
			if event.key == pygame.K_RIGHT:
				change_to = const.RIGHT
		if event.type == pygame.QUIT:
			game_over = True

	if change_to == const.UP and direction != const.DOWN:
		direction = const.UP
	if change_to == const.DOWN and direction != const.UP:
		direction = const.DOWN
	if change_to == const.LEFT and direction != const.RIGHT:
		direction = const.LEFT
	if change_to == const.RIGHT and direction != const.LEFT:
		direction = const.RIGHT

	snake_body.insert(0, list(snake_head_position))

	if direction == const.UP:
		snake_head_position[1] -= square_size
	if direction == const.DOWN:
		snake_head_position[1] += square_size
	if direction == const.LEFT:
		snake_head_position[0] -= square_size
	if direction == const.RIGHT:
		snake_head_position[0] += square_size
	
	if snake_head_position[0] == food_position[0] and snake_head_position[1] == food_position[1]:
		food_spawn = False
		score += 1
	else:
		snake_body.pop()

	if snake_head_position[0] < 0 or snake_head_position[0] > window_size[0] - square_size:
		game_over = True
	if snake_head_position[1] < 0 or snake_head_position[1] > window_size[1] - square_size:
		game_over = True
	for block in snake_body[1:]:
		if snake_head_position[0] == block[0] and snake_head_position[1] == block[1]:
			game_over = True
	
	if not food_spawn:
		food_position = [
			random.randrange(1, (window_size[0] // square_size)) * square_size,
			random.randrange(1, (window_size[1] // square_size)) * square_size
		]
		food_spawn = True

	screen.fill(background_color)

	pygame.draw.rect(
		screen,
		snake_color,
		pygame.Rect(snake_head_position[0], snake_head_position[1], square_size, square_size)
	)
 
	for pos in snake_body:
		pygame.draw.rect(
			screen,
			snake_color,
			pygame.Rect(pos[0], pos[1], square_size, square_size)
		)

	pygame.draw.rect(
		screen,
		food_color,
		pygame.Rect(food_position[0], food_position[1], square_size, square_size)
	)

	score_font = font.render("Score: " + str(score), True, score_color)
	screen.blit(score_font, (5, 10))

	pygame.display.update()

	clock.tick(fps * game_speed)


pygame.quit()


print("Game Over")