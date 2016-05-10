import tensorflow as tf
import numpy as np
from collections import deque
import random
import cv2
import reward
from problemIO import problemreader
from simulator import nextstate
import action
import state
import train

class test(object):
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

        # set the first action to do nothing
        self._last_action = np.zeros(self.ACTIONS_COUNT)

        self._last_state = None

        self._session.run(tf.initialize_all_variables())


    def _test(self, test_data):
        for problem_set in test_data:
            total_cycletime = 0.0

            sht = problem_set.shuttleNum
            clm = problem_set.columnNum
            flr = problem_set.floorNum

            rack = problem_set.rack.status

            rack_resized = state.get_storage_binary(rack)
            rack_resized = self.change_to_two_dimension(rack_resized, clm, flr)
            rack_resized = np.array(rack_resized)

            # scale down game image
            rack_resized = cv2.resize(rack_resized, (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y))

            # first frame must be handled differently
            self._last_state = np.stack(tuple(rack_resized for _ in range(self.STATE_FRAMES)), axis=2)

            cycleNum = problem_set.requestLength / sht

            for order_idx in range(cycleNum):
                input = problem_set.input[order_idx * sht:order_idx * sht + sht]
                output = problem_set.output[order_idx * sht:order_idx * sht + sht]

                self._last_action = self._choose_next_action()

                for i in range(len(self._last_action)):
                    if self._last_action[i] == 1:
                        action_chosen = i
                        break

                at = action.action()

                solution, cycletime = at.dijk_idx(rack, clm, flr, input, output, action_chosen)

                sim = nextstate.simul()

                rack = sim.change_rs(rack, clm, flr, solution)

                rack_resized = state.get_storage_binary(rack)
                rack_resized = self.change_to_two_dimension(rack_resized, clm, flr)
                rack_resized = np.array(rack_resized)

                # scale down game image
                rack_resized = cv2.resize(rack_resized, (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y))

                rack_resized = np.reshape(rack_resized,
                                          (self.RESIZED_SCREEN_X, self.RESIZED_SCREEN_Y, 1))

                current_state = np.append(rack_resized, self._last_state[:, :, 1:], axis=2)

                # update the old values
                self._last_state = current_state

                total_cycletime += cycletime
            print total_cycletime


    def _choose_next_action(self):
        new_action = np.zeros([self.ACTIONS_COUNT])

        # choose an action given our last state
        readout_t = self._session.run(self._output_layer, feed_dict={self._input_layer: [self._last_state]})[0]
        action_index = np.argmax(readout_t)

        new_action[action_index] = 1
        return new_action


    def change_to_two_dimension(self, rack_status, columnNum, floorNum):
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[row * floorNum + col]
        return result


if __name__ == '__main__':
    tr = train.train()
    pr = problemreader.ProblemReader(20)
    input, output = tr._train(pr.get_problems(3))
    te = test(input, output)
    pr2 = problemreader.ProblemReader(21)
    te._test(pr2.get_problems(3))