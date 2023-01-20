import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from os import path

from keras.models import load_model, Sequential
from keras.layers import Dense, Dropout, Input
from keras.activations import relu, softmax
from keras.metrics import Accuracy

from const import directions

class SnakeAgent:
	def __init__(s) -> None:
		s.agent_output = len(directions)
		s.learning_rate = 0.0001
		s.discount_factor = 0.9
		s.model = s.build_model()
		pass

	def get_model(s):
		return s.model

	def build_model(s):
		if path.exists('snake_ai.h5'):
			model = load_model('snake_ai.h5')
		else:
			model = Sequential([
				Input(shape=(432,)),
				Dense(256, activation=relu),
				Dropout(0.2),
				Dense(128, activation=relu),
				Dropout(0.2),
				Dense(s.agent_output, activation=softmax)
			])

			model.compile(
				tf.optimizers.Adam(s.learning_rate),
				loss = tf.losses.mean_squared_error
			)
		return model

	def preprogess(s, state):
		state = np.array(state)
		# Reshape the state array into an (1, n) array
		# with n is the number in 1 * n = total number of element in state array
		state = state.reshape(1, -1)
  
		return state

	def act(s, state):
		action_probs = s.model.predict(state)
		action = np.random.choice(s.agent_output, p=action_probs[0])
		return action

	def update_model(s, state, action, reward, done, next_state):
		# Get the current Q-value for the state-action pair
		current_q_value = s.model.predict(state)

		# If the game is done, the Q-value for the current state-action pair is just the reward
		if done:
			current_q_value[0][action] = reward
		else:
			# Get the maximum Q-value for the next state
			next_q_value = s.model.predict(next_state)
			max_next_q_value = max(next_q_value[0])

			# Q(s, a) = Q(s, a) + α * (r + γ * max(Q(s', a')) - Q(s, a))
			# Where:
				# Q(s, a) is the current estimate of the Q-value for state s and action a
				# α is the learning rate
				# r is the reward received from taking action a in state s
				# γ is the discount factor
				# max(Q(s', a')) is the maximum estimated Q-value for the next state s' and all possible actions a'
		
				# Update the current Q-value using the Bellman equation
			current_q_value[0][action] = current_q_value[0][action] + s.learning_rate * (reward + s.discount_factor * max_next_q_value - current_q_value[0][action])

		# Fit the model with the updated Q-value for the current state-action pair
		s.model.fit(state, current_q_value, epochs=1, verbose=0)