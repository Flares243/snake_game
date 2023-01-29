from snake_agent import SnakeAgent
from snake_enviroment import SnakeEnviroment
from generic_algo import GenericAlgoOptimizer

# Main function to run the optimization
if __name__ == "__main__":
	# Initialize the environment and the agent
	agent = SnakeAgent()
	env = SnakeEnviroment()

	# Create an instance of the optimizer
	optimizer = GenericAlgoOptimizer(env, agent)
	# Start the optimization
	optimizer.optimize()
 