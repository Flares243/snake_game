from snake_enviroment import SnakeEnviroment
from snake_agent import SnakeAgent
from keras.models import save_model

env = SnakeEnviroment()
agent = SnakeAgent()

play_rounds = 200

for play_round in range(play_rounds):
	state = env.initialize()
	state = agent.preprogess(state)

	done = False

	while not done:
		action = agent.act(state)
		next_state, reward, done, info = env.step(action)		
		next_state = agent.preprogess(next_state)
		agent.update_model(state, action, reward, done, next_state)
		state = next_state
		env.render()
  
save_model(agent.get_model(), 'snake_ai.h5')