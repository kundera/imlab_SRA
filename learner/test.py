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
import actiongenerator

class test(object):
    ACTIONS_COUNT = 5  # number of valid actions.
    STATE_FRAMES = 4  # number of frames to store in the state
    RESIZED_SCREEN_X, RESIZED_SCREEN_Y = (80, 80)


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
                sol, cyc = at.dijk(rack, clm, flr, input, output)

                atg = actiongenerator.ActionGenerator()
                solution, cycletime = atg.generating_idx(rack, clm, flr, sol, action_chosen)

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
    input, output = tr._train(pr.get_problems(10))
    te = test(input, output)
    pr2 = problemreader.ProblemReader(20)
    te._test(pr2.get_problems(3))