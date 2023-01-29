from snake_enviroment import SnakeEnviroment
from snake_agent import SnakeAgent
from keras.models import load_model, Sequential
import tensorflow as tf

env = SnakeEnviroment()
agent = SnakeAgent()

agent.model.load_weights('snake_ai.pth')

play_rounds = 500

for episole in range(play_rounds):
	state = env.initialize()
	state = env.preprogess(state)

	done = False

	while not done:
		action = agent.act(state)
		next_state, reward, done, info = env.step(action)		
		state = env.preprogess(next_state)
		env.render()