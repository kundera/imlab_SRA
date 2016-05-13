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
import actiongenerator

class ASRSplayer(object):
    ACTIONS_COUNT = 4  # number of valid actions.
    FUTURE_REWARD_DISCOUNT = 0.99  # decay rate of past observations
    EXPLORE_STEPS = 2000000.  # frames over which to anneal epsilon
    INITIAL_RANDOM_ACTION_PROB = 1.0  # starting chance of an action being random
    FINAL_RANDOM_ACTION_PROB = 0.05  # final chance of an action being random
    MINI_BATCH_SIZE = 32  # size of mini batches
    STATE_FRAMES = 6  # number of frames to store in the state
    COLUMN, FLOOR = (80,80)
    OBS_LAST_STATE_INDEX, OBS_ACTION_INDEX, OBS_REWARD_INDEX, OBS_CURRENT_STATE_INDEX, OBS_TERMINAL_INDEX = range(5)
    LEARN_RATE = 1e-6
    ITERATION = 10000


    def __init__(self):

        self._session = tf.Session()
        self._input_layer, self._output_layer = ASRSplayer._create_network()

        self._action = tf.placeholder("float", [None, self.ACTIONS_COUNT])
        self._target = tf.placeholder("float", [None])

        readout_action = tf.reduce_sum(tf.mul(self._output_layer, self._action), reduction_indices=1)

        cost = tf.reduce_mean(tf.square(self._target - readout_action))
        self._train_operation = tf.train.AdamOptimizer(self.LEARN_RATE).minimize(cost)

        # set the first action to do nothing
        self._last_action = np.zeros(self.ACTIONS_COUNT)

        self._last_state = None
        self._probability_of_random_action = self.INITIAL_RANDOM_ACTION_PROB

        self._session.run(tf.initialize_all_variables())
        #self._observations = _observations


    def _train(self, training_data):

        iter = 0

        while iter < self.ITERATION:

            total_cycletime = 0.0

            sht = training_data.shuttleNum
            clm = training_data.columnNum
            flr = training_data.floorNum

            rack = training_data.rack.status

            input = training_data.input[0:0 + sht]
            output = training_data.output[0:0 + sht]

            rack_str = state.get_storage_binary(rack)
            rack_ret = state.get_retrieval_binary(rack, output)

            rack_str = self.change_to_two_dimension(rack_str, clm, flr)
            rack_sr = rack_str

            for i in range(len(rack_ret)):
                rack_sr = np.append(rack_sr, self.change_to_two_dimension(rack_ret[i], clm, flr), axis = 2)

            self._last_state = rack_sr

            cycleNum = training_data.requestLength / sht

            for order_idx in range(cycleNum):
                self._last_action = self._choose_next_action()

                for i in range(len(self._last_action)):
                    if self._last_action[i] == 1:
                        action_chosen = i
                        break

                at = action.action()
                solution, cycletime = at.dijk_idx(rack, clm, flr, input, output, action_chosen)

                sim = nextstate.simul()

                rack = sim.change_rs(rack, clm, flr, solution)

                input = training_data.input[order_idx * sht:order_idx * sht + sht]
                output = training_data.output[order_idx * sht:order_idx * sht + sht]

                rack_str = state.get_storage_binary(rack)
                rack_ret = state.get_retrieval_binary(rack, output)

                rack_str = self.change_to_two_dimension(rack_str, clm, flr)
                rack_sr = rack_str

                for i in range(len(rack_ret)):
                    rack_sr = np.append(rack_sr, self.change_to_two_dimension(rack_ret[i], clm, flr), axis=2)

                current_state = rack_sr

                if order_idx == cycleNum-1:
                    terminal = True
                else:
                    terminal = False

                # store the transition in previous_observations
                self._observations.append((self._last_state, self._last_action, cycletime/reward.reward().get_maxtime\
                    (clm, flr, sht), current_state, terminal))

                self._observations.popleft()

                # sample a mini_batch to train on
                mini_batch = random.sample(self._observations, self.MINI_BATCH_SIZE)
                # get the batch variables
                previous_states = [d[self.OBS_LAST_STATE_INDEX] for d in mini_batch]
                actions = [d[self.OBS_ACTION_INDEX] for d in mini_batch]
                rewards = [d[self.OBS_REWARD_INDEX] for d in mini_batch]
                current_states = [d[self.OBS_CURRENT_STATE_INDEX] for d in mini_batch]
                agents_expected_reward = []
                # this gives us the agents expected reward for each action we might
                agents_reward_per_action = self._session.run(self._output_layer,
                                                             feed_dict={self._input_layer: current_states})
                for i in range(len(mini_batch)):
                    if mini_batch[i][self.OBS_TERMINAL_INDEX]:
                        # this was a terminal frame so need so scale future reward...
                        agents_expected_reward.append(rewards[i])
                    else:
                        agents_expected_reward.append(
                            rewards[i] + self.FUTURE_REWARD_DISCOUNT * np.max(agents_reward_per_action[i]))

                # learn that these actions in these states lead to this reward
                self._session.run(self._train_operation, feed_dict={
                    self._input_layer: previous_states,
                    self._action: actions,
                    self._target: agents_expected_reward})

                # update the old values
                self._last_state = current_state

                # gradually reduce the probability of a random actionself.
                if self._probability_of_random_action > self.FINAL_RANDOM_ACTION_PROB:
                    self._probability_of_random_action -= \
                        (self.INITIAL_RANDOM_ACTION_PROB - self.FINAL_RANDOM_ACTION_PROB) / self.EXPLORE_STEPS

                total_cycletime += cycletime
            iter += 1
            print iter, total_cycletime


    def _choose_next_action(self):
        new_action = np.zeros([self.ACTIONS_COUNT])

        if random.random() <= self._probability_of_random_action:
            # choose an action randomly
            action_index = random.randrange(self.ACTIONS_COUNT)
        else:
            # choose an action given our last state
            readout_t = self._session.run(self._output_layer, feed_dict={self._input_layer: [self._last_state]})[0]
            action_index = np.argmax(readout_t)

        new_action[action_index] = 1
        return new_action


    def change_to_two_dimension(self, rack_status, columnNum, floorNum):
        leftrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                leftrack[clm][flr] = rack_status[clm * floorNum + flr]
        rightrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                rightrack[clm][flr] = rack_status[columnNum * floorNum + clm * floorNum + flr]

        result = np.append(np.reshape(np.array(leftrack), (columnNum, floorNum, 1)), np.reshape(np.array(rightrack), (columnNum, floorNum, 1)), axis=2)
        return result


    @staticmethod
    def _create_network():
        # network weights
        convolution_weights_1 = tf.Variable(tf.truncated_normal([8, 8, ASRSplayer.STATE_FRAMES, 32], stddev=0.01))
        convolution_bias_1 = tf.Variable(tf.constant(0.01, shape=[32]))

        convolution_weights_2 = tf.Variable(tf.truncated_normal([4, 4, 32, 64], stddev=0.01))
        convolution_bias_2 = tf.Variable(tf.constant(0.01, shape=[64]))

        convolution_weights_3 = tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01))
        convolution_bias_3 = tf.Variable(tf.constant(0.01, shape=[64]))

        feed_forward_weights_1 = tf.Variable(tf.truncated_normal([1600, 256], stddev=0.01))
        feed_forward_bias_1 = tf.Variable(tf.constant(0.01, shape=[256]))

        feed_forward_weights_2 = tf.Variable(tf.truncated_normal([256, ASRSplayer.ACTIONS_COUNT], stddev=0.01))
        feed_forward_bias_2 = tf.Variable(tf.constant(0.01, shape=[ASRSplayer.ACTIONS_COUNT]))

        input_layer = tf.placeholder("float", [None, ASRSplayer.COLUMN, ASRSplayer.FLOOR,
                                               ASRSplayer.STATE_FRAMES])

        hidden_convolutional_layer_1 = tf.nn.relu(
            tf.nn.conv2d(input_layer, convolution_weights_1, strides=[1, 4, 4, 1],
                         padding="SAME") + convolution_bias_1)

        hidden_max_pooling_layer = tf.nn.max_pool(hidden_convolutional_layer_1, ksize=[1, 2, 2, 1],
                                                  strides=[1, 2, 2, 1], padding="SAME")

        hidden_convolutional_layer_2 = tf.nn.relu(
            tf.nn.conv2d(hidden_max_pooling_layer, convolution_weights_2, strides=[1, 2, 2, 1],
                         padding="SAME") + convolution_bias_2)

        hidden_convolutional_layer_3 = tf.nn.relu(
            tf.nn.conv2d(hidden_convolutional_layer_2, convolution_weights_3,
                         strides=[1, 1, 1, 1], padding="SAME") + convolution_bias_3)

        hidden_convolutional_layer_3_flat = tf.reshape(hidden_convolutional_layer_3, [-1, 1600])

        final_hidden_activations = tf.nn.relu(
            tf.matmul(hidden_convolutional_layer_3_flat, feed_forward_weights_1) + feed_forward_bias_1)

        output_layer = tf.matmul(final_hidden_activations, feed_forward_weights_2) + feed_forward_bias_2

        return input_layer, output_layer


if __name__ == '__main__':
    pl = ASRSplayer()
    pr = problemreader.ProblemReader(20)
    pl._train(pr.get_problem(1))