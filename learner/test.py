import numpy as np
import random

ACTIONS_COUNT = 2  # number of valid actions.
FUTURE_REWARD_DISCOUNT = 0.99  # decay rate of past observations
OBSERVATION_STEPS = 500000.  # time steps to observe before training
EXPLORE_STEPS = 2000000.  # frames over which to anneal epsilon
INITIAL_RANDOM_ACTION_PROB = 1.0  # starting chance of an action being random
FINAL_RANDOM_ACTION_PROB = 0.05  # final chance of an action being random
MEMORY_SIZE = 590000  # number of observations to remember
MINI_BATCH_SIZE = 32  # size of mini batches
STATE_FRAMES = 4  # number of frames to store in the state
RESIZED_SCREEN_X, RESIZED_SCREEN_Y = (80, 80)
OBS_LAST_STATE_INDEX, OBS_ACTION_INDEX, OBS_REWARD_INDEX, OBS_CURRENT_STATE_INDEX, OBS_TERMINAL_INDEX = range(5)
SAVE_EVERY_X_STEPS = 10000
LEARN_RATE = 1e-6
STORE_SCORES_LEN = 200.

class test:

    def _choose_next_action(self):
        new_action = np.zeros([self.ACTIONS_COUNT])

        if self._playback_mode or (random.random() <= self._probability_of_random_action):
            # choose an action randomly
            action_index = random.randrange(self.ACTIONS_COUNT)
        else:
            # choose an action given our last state
            readout_t = self._session.run(self._output_layer, feed_dict={self._input_layer: [self._last_state]})[0]
            action_index = np.argmax(readout_t)

        new_action[action_index] = 1
        return new_action