import tensorflow as tf
import numpy as np

from os import path

from keras.models import load_model, Sequential
from keras.layers import Dense, Dropout, Input
from keras.activations import relu, softmax

from const import directions

class SnakeAgent:
	def __init__(s) -> None:
		s.agent_output = len(directions)
		s.model = s.build_model()
		pass

	def build_model(s):
		if path.exists('snake_ai.h5'):
			model = load_model('snake_ai.h5')
		else:
			model = Sequential([
				Input(shape=(200,)),
				Dense(128, activation=relu),
				Dropout(0.1),
				Dense(64, activation=relu),
				Dropout(0.1),
				Dense(s.agent_output, activation=softmax)
			])
			model.compile(
				tf.optimizers.Adam(0.001),
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
		if done:
				target = reward
		else:
				next_q_value = s.model.predict(next_state)[0]
				target = reward + 0.9 * np.max(next_q_value)

		target_vec = s.model.predict(state)
		target_vec[0][action] = target

		s.model.fit(state, target_vec, epochs=1, verbose=0)