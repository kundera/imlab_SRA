import tensorflow as tf
import numpy as np
from collections import deque
import random
import cv2
import reward
from problemIO import problemreader
from simulator import Simulator
import action
import state
import train

class test:
    ACTIONS_COUNT = 4  # number of valid actions.
    FUTURE_REWARD_DISCOUNT = 0.99  # decay rate of past observations
    OBSERVATION_STEPS = 32.  # time steps to observe before test
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


    def __init__(self, _input_layer, _output_layer):
        self._session = tf.Session()
        self._input_layer = _input_layer
        self._output_layer = _output_layer

        self._action = tf.placeholder("float", [None, self.ACTIONS_COUNT])
        self._target = tf.placeholder("float", [None])

        readout_action = tf.reduce_sum(tf.mul(self._output_layer, self._action), reduction_indices=1)

        cost = tf.reduce_mean(tf.square(self._target - readout_action))
        self._train_operation = tf.train.AdamOptimizer(self.LEARN_RATE).minimize(cost)

        self._observations = deque()

        # set the first action to do nothing
        self._last_action = np.zeros(self.ACTIONS_COUNT)

        self._last_state = None
        self._probability_of_random_action = self.INITIAL_RANDOM_ACTION_PROB

        self._session.run(tf.initialize_all_variables())


    def _choose_next_action(self):
        new_action = np.zeros([self.ACTIONS_COUNT])

        # choose an action given our last state
        readout_t = self._session.run(self._output_layer, feed_dict={self._input_layer: [self._last_state]})[0]
        action_index = np.argmax(readout_t)

        new_action[action_index] = 1
        return new_action


    def _test(self, test_data):
        cycleNum = test_data.requestLength / test_data.shuttleNum
        rack = test_data.rack
        rack_status = self.change_to_two_dimension(test_data.rack, test_data.columnNum, test_data.floorNum)
        rack_status = state.get_storage_binary(rack_status)
        rack_status = np.array(rack_status)

        # scale down game image
        screen_resized = cv2.resize(rack_status, (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y))

        # first frame must be handled differently
        self._last_state = np.stack(tuple(screen_resized for _ in range(self.STATE_FRAMES)), axis=2)

        total_cycletime = 0.0

        for order_idx in range(cycleNum):
            input = test_data.input.split(", ")[
                    order_idx * test_data.shuttleNum:order_idx * test_data.shuttleNum + test_data.shuttleNum]
            output = test_data.output.split(", ")[
                     order_idx * test_data.shuttleNum:order_idx * test_data.shuttleNum + test_data.shuttleNum]

            self._last_action = self._choose_next_action()

            for i in range(len(self._last_action)):
                if self._last_action[i] == 1:
                    action_index = i
                    break
            at = action.action()

            a1, a2, a3, a4 = at.dijk_idx(rack.split(", "), test_data.columnNum, test_data.floorNum, input, output,
                                         action_index)

            a = []
            for i in range(len(a1)):
                a.append(a1[i])
            for i in range(len(a2)):
                a.append(a2[i])
            for i in range(len(a3)):
                a.append(a3[i])

            sim = Simulator.simul()

            rack_array = sim.change_rs(rack, a)
            rack = ''
            for i in range(len(rack_array)):
                rack += rack_array[i] + ", "
            rack = rack[:-2]

            rack_status = self.change_to_two_dimension(rack, test_data.columnNum, test_data.floorNum)
            rack_status = state.get_storage_binary(rack_status)
            rack_status = np.array(rack_status)

            # scale down game image
            screen_resized = cv2.resize(rack_status, (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y))

            screen_resized = np.reshape(screen_resized,
                                        (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y, 1))

            current_state = np.append(screen_resized, self._last_state[:, :, 1:], axis=2)

            # update the old values
            self._last_state = current_state

            total_cycletime += a4

        return total_cycletime


if __name__ == '__main__':
    tr = train.train()
    pr = problemreader.ProblemWithSolutionReader(10,1)
    te = test(tr._train(pr.get_problem_with_solution()))
    pr = problemreader.ProblemWithSolutionReader(11,1)
    print te._test(pr.get_problem_with_solution())