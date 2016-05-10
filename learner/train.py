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

class train(object):
    ACTIONS_COUNT = 5  # number of valid actions.
    FUTURE_REWARD_DISCOUNT = 0.99  # decay rate of past observations
    OBSERVATION_STEPS = 33.  # time steps to observe before training
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

    def __init__(self):

        self._session = tf.Session()
        self._input_layer, self._output_layer = train._create_network()

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


    def _train(self, training_data):
        for problem_set in training_data:
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

                if order_idx == cycleNum-1:
                    terminal = True
                else:
                    terminal = False

                # store the transition in previous_observations
                self._observations.append((self._last_state, self._last_action, cycletime/reward.reward().get_maxtime(clm, flr, sht), current_state, terminal))

                if len(self._observations) > self.MEMORY_SIZE:
                    self._observations.popleft()

                # only train if done observing
                if len(self._observations) > self.OBSERVATION_STEPS:
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
                if self._probability_of_random_action > self.FINAL_RANDOM_ACTION_PROB \
                        and len(self._observations) > self.OBSERVATION_STEPS:
                    self._probability_of_random_action -= \
                        (self.INITIAL_RANDOM_ACTION_PROB - self.FINAL_RANDOM_ACTION_PROB) / self.EXPLORE_STEPS

            return self._input_layer, self._output_layer


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
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[row * floorNum + col]
        return result


    @staticmethod
    def _create_network():
        # network weights
        convolution_weights_1 = tf.Variable(tf.truncated_normal([8, 8, train.STATE_FRAMES, 32], stddev=0.01))
        convolution_bias_1 = tf.Variable(tf.constant(0.01, shape=[32]))

        convolution_weights_2 = tf.Variable(tf.truncated_normal([4, 4, 32, 64], stddev=0.01))
        convolution_bias_2 = tf.Variable(tf.constant(0.01, shape=[64]))

        convolution_weights_3 = tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01))
        convolution_bias_3 = tf.Variable(tf.constant(0.01, shape=[64]))

        feed_forward_weights_1 = tf.Variable(tf.truncated_normal([1600, 256], stddev=0.01))
        feed_forward_bias_1 = tf.Variable(tf.constant(0.01, shape=[256]))

        feed_forward_weights_2 = tf.Variable(tf.truncated_normal([256, train.ACTIONS_COUNT], stddev=0.01))
        feed_forward_bias_2 = tf.Variable(tf.constant(0.01, shape=[train.ACTIONS_COUNT]))

        input_layer = tf.placeholder("float", [None, train.RESIZED_SCREEN_X, train.RESIZED_SCREEN_Y,
                                               train.STATE_FRAMES])

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
    tr = train()
    pr = problemreader.ProblemReader(20)
    tr._train(pr.get_problems(3))