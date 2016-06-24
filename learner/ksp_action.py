import ksp
import action
from problemIO import problemreader
from simulator import nextstate
from simulator import visualize_rack
import matplotlib.pyplot as plt
import copy

class KSP_ACTION(object, ksp.KSP):

    def select_action_considering_sr_shortest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self,[0,0,0],k_sols[i].loc[0])+
                                          ksp.KSP.get_time(self,[0,0,0],k_sols[i].loc[1])+
                                          ksp.KSP.get_time(self,[0,0,0],k_sols[i].loc[2])+
                                          ksp.KSP.get_time(self,[0,0,0],k_sols[i].loc[3]))/4)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == min(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_sr_longest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0])+
                                          ksp.KSP.get_time(self,[0,0,0],k_sols[i].loc[1])+
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[2])+
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[3])) / 4)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == max(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_s_shortest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]) +
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[2]))/2)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == min(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_s_longest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]) +
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[2])) / 2)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == max(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_r_shortest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[1]) +
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[3])) / 2)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == min(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_r_longest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append((ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[1]) +
                                          ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[3])) / 2)

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == max(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_first_s_shortest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append(ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]))

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == min(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_first_s_longest(self, rs, column, floor, input, output, k):
        # k means finding solutions optimal cycletime + k
        get_average_time_list = []
        k_sols, k_times = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output, k)

        for i in range(len(k_sols)):
            get_average_time_list.append(ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]))

        for i in range(len(get_average_time_list)):
            if get_average_time_list[i] == max(get_average_time_list):
                return k_sols[i], k_times[i]

    def select_action_considering_sr_shortest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime= self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime= self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_sr_longest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_s_shortest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_s_longest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_r_shortest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_r_longest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_first_s_shortest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

    def select_action_considering_first_s_longest_density(self, rs, column, floor, input, output, k, idx):
        if idx == 0:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 1:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 2:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

        if idx == 3:
            if input[0] <= input[1] and output[0] <= output[1]:
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[0] <= output[1]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[1] < input[0] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)

                return sol, cycletime
            
    def select_action_considering_sr_shortest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_sr_shortest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_sr_shortest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_sr_shortest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_sr_shortest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
        
    def select_action_considering_sr_longest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_sr_longest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_sr_longest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_sr_longest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_sr_longest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h

    def select_action_considering_s_shortest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_s_shortest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_s_shortest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_s_shortest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_s_shortest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
        
    def select_action_considering_s_longest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_s_longest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_s_longest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_s_longest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_s_longest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
        
    def select_action_considering_r_shortest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_r_shortest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_r_shortest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_r_shortest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_r_shortest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
        
    def select_action_considering_r_longest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_r_longest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_r_longest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_r_longest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_r_longest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
        
    def select_action_considering_first_s_shortest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_first_s_shortest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_first_s_shortest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_first_s_shortest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_first_s_shortest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h
    
    def select_action_considering_first_s_longest_density_best(self, rs, column, floor, input, output, k):
        a, b = self.select_action_considering_first_s_longest_density(rs, column, floor, input, output, k, 0)
        c, d = self.select_action_considering_first_s_longest_density(rs, column, floor, input, output, k, 1)
        e, f = self.select_action_considering_first_s_longest_density(rs, column, floor, input, output, k, 2)
        g, h = self.select_action_considering_first_s_longest_density(rs, column, floor, input, output, k, 3)
        
        cycletimes = [b,d,f,h]
        
        if b == min(cycletimes):
            return a,b
        elif d == min(cycletimes):
            return c,d
        elif f == min(cycletimes):
            return e,f
        elif h == min(cycletimes):
            return g,h

    def actions_test(self, rs,column,floor,input,output,k,index):
        ac = action.action()
        if index == 0:
            sol,cycletime = ac.dijk(rs,column,floor,input,output)
            return sol, cycletime
        elif index == 1:
            sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 2:
            sol, cycletime = self.select_action_considering_sr_longest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 3:
            sol, cycletime = self.select_action_considering_s_shortest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 4:
            sol, cycletime = self.select_action_considering_s_longest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 5:
            sol, cycletime = self.select_action_considering_r_shortest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 6:
            sol, cycletime = self.select_action_considering_r_longest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 7:
            sol, cycletime = self.select_action_considering_first_s_shortest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 8:
            sol, cycletime = self.select_action_considering_first_s_longest(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 9:
            sol, cycletime = self.select_action_considering_sr_shortest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 10:
            sol, cycletime = self.select_action_considering_sr_longest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 11:
            sol, cycletime = self.select_action_considering_s_shortest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 12:
            sol, cycletime = self.select_action_considering_s_longest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 13:
            sol, cycletime = self.select_action_considering_r_shortest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 14:
            sol, cycletime = self.select_action_considering_r_longest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 15:
            sol, cycletime = self.select_action_considering_first_s_shortest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime
        elif index == 16:
            sol, cycletime = self.select_action_considering_first_s_longest_density_best(rs, column, floor, input, output, k)
            return sol, cycletime

    def reducing_sols(self, k_sols, k_times):

        if len(k_times) == 1:
            sol = k_sols[0]
            time = k_times[0]

        else:
            for i in range(len(k_times)):
                if i == 0:
                    path_list = []
                    path_times = []
                    first_in = ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0])
                    path_list.append(k_sols[i])
                    path_times.append(k_times[i])
                else:
                    if first_in == ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]):
                        path_list.append(k_sols[i])
                        path_times.append(k_times[i])
                    elif first_in < ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0]):
                        path_list = []
                        path_times = []
                        first_in = ksp.KSP.get_time(self, [0, 0, 0], k_sols[i].loc[0])
                        path_list.append(k_sols[i])
                        path_times.append(k_times[i])

            if len(path_list) == 1:
                sol = path_list[0]
                time = path_times[0]
            else:
                for i in range(len(path_times)):
                    if i == 0:
                        sols = []
                        times = []
                        sols.append(path_list[i])
                        times.append(path_times[i])
                        second_out = ksp.KSP.get_time(self, [0, 0, 0], path_list[i].loc[3])
                    else:
                        if second_out == ksp.KSP.get_time(self, [0, 0, 0], path_list[i].loc[3]):
                            sols.append(path_list[i])
                            times.append(path_times[i])
                        elif second_out > ksp.KSP.get_time(self, [0, 0, 0], path_list[i].loc[3]):
                            sols = []
                            times = []
                            sols.append(path_list[i])
                            times.append(path_times[i])
                            second_out = ksp.KSP.get_time(self, [0, 0, 0], path_list[i].loc[3])
                if len(times) == 1:
                    sol = sols[0]
                    time = times[0]
                else:
                    for i in range(len(times)):
                        if i == 0:
                            sol = sols[0]
                            time = times[0]
                        else:
                            if ksp.KSP.get_time(self, [0, 0, 0], sol.loc[1]) > ksp.KSP.get_time(self, [0, 0, 0], sols[i].loc[1]):
                                sol = sols[i]
                                time = times[i]

        return sol, time

    def final_action_test1(self, rs, column, floor, input, output, k, index):
        if index == 0:
            if input[0] >= input[1]:
                input = [input[0], input[1]]
            elif input[0] < input[1]:
                input = [input[1], input[0]]
        elif index == 1:
            if input[0] >= input[1]:
                input = [input[1], input[0]]
            elif input[0] < input[1]:
                input = [input[0], input[1]]
        elif index == 2:
            input = [input[0], input[1]]

        output1 = [output[0], output[1]]
        output2 = [output[1], output[0]]

        k_sols1, k_times1 = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output1, k)
        sol1, time1 = self.reducing_sols(k_sols1, k_times1)

        k_sols2, k_times2 = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output2, k)
        sol2, time2 = self.reducing_sols(k_sols2, k_times2)

        if time1 > time2:
            return sol2, time2
        else:
            return sol1, time1

    def final_action_test2(self, rs, column, floor, input, output, k, index):
        if input[0] >= input[1]:
            input = [input[0], input[1]]
        elif input[0] < input[1]:
            input = [input[1], input[0]]

        output1 = [output[0], output[1]]
        output2 = [output[1], output[0]]

        k_sols1, k_times1 = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output1, k)
        sol1, time1 = self.reducing_sols(k_sols1, k_times1)

        k_sols2, k_times2 = ksp.KSP.k_shortest_path(self, rs, column, floor, input, output2, k)
        sol2, time2 = self.reducing_sols(k_sols2, k_times2)

        if time1 > time2:
            sol = sol2
            time = time2
        else:
            sol = sol1
            time = time1

        loc0 = ksp.KSP.get_time(self, [0, 0, 0], sol.loc[0])
        loc2 = ksp.KSP.get_time(self, [0, 0, 0], sol.loc[2])
        if index == 0:
            if loc0 >= loc2:
                sol.type[0] = input[0]
                sol.type[2] = input[1]
            else:
                sol.type[0] = input[1]
                sol.type[2] = input[0]
        elif index == 1:
            if loc0 >= loc2:
                sol.type[0] = input[1]
                sol.type[2] = input[0]
            else:
                sol.type[0] = input[0]
                sol.type[2] = input[1]

        return sol, time

    def final(self, rs, column, floor, input, output, k, index):
        if index == 0:
            return self.final_action_test1(rs, column, floor, input, output, k, 0)
        elif index == 1:
            return self.final_action_test1(rs, column, floor, input, output, k, 1)
        elif index == 2:
            return self.final_action_test2(rs, column, floor, input, output, k, 0)
        elif index == 3:
            return self.final_action_test2(rs, column, floor, input, output, k, 1)
        elif index == 4:
            return self.final_action_test1(rs, column, floor, input, output, k, 2)
        elif index == 5:
            ts = action.action()
            return ts.dijk(rs, column, floor, input, output)


if __name__ == '__main__':

    # probnum = 28
    # pronum = 10
    # test = problemreader.ProblemReader(probnum)
    # rs = test.get_problem(pronum).rack.status
    # column = test.get_problem(pronum).rack.column
    # floor = test.get_problem(pronum).rack.floor
    # input = test.get_problem(pronum).input
    # output = test.get_problem(pronum).output
    #
    # vi = visualize_rack.visualize()
    # ts = action.action()
    # ka = KSP_ACTION()
    # sm = nextstate.simul()
    # cycletime0 = 0
    #
    # rs0 = copy.deepcopy(rs)
    # size = len(input) / 2
    # # size = 100
    #
    # temp = 1
    # k = 0
    # ite = 10
    # vi.comparison_visual(rs0, column, floor, temp)
    #
    #
    # for i in range(size):
    #     inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
    #     outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]
    #
    #     # a, b = ka.actions_test(rs0, column, floor, inputs, outputs, k, ite)
    #     # a, b = ts.dijk(rs0, column, floor, inputs, outputs)
    #     a, b = ka.final(rs0, column, floor, inputs, outputs, k, 1)
    #     cycletime0 += b
    #     rs0 = sm.change_rs(rs0, column, floor, a)
    #
    #     print i, a.type, a.loc
    #
    #     if i % (size / 7) == 0:
    #         temp += 1
    #         vi.comparison_visual(rs0, column, floor, temp)
    #
    #
    # plt.show()

    probnum = 28
    pronum = 1

    k = 0

    ka = KSP_ACTION()
    ts = action.action()
    sm = nextstate.simul()


    while pronum < 21:

        if pronum == 10:
            continue

        for i in range(0, 6):
            if i != 2 and i != 4:
                continue
            test = problemreader.ProblemReader(probnum)
            rs = test.get_problem(pronum).rack.status
            column = test.get_problem(pronum).rack.column
            floor = test.get_problem(pronum).rack.floor
            input = test.get_problem(pronum).input
            output = test.get_problem(pronum).output

            rs0 = copy.deepcopy(rs)
            cycletime = 0
            for cycle in range(len(input)/2):
                inputs = input[(cycle+1)*2-2:(cycle+1)*2]
                outputs = output[(cycle + 1) * 2 - 2:(cycle + 1) * 2]
                sol, b = ka.final(rs0, column, floor, inputs, outputs, k, i)
                # sol, b = ts.dijk(rs0, column, floor, inputs, outputs)
                rs0 = sm.change_rs(rs0, column, floor, sol)
                cycletime += b
            print pronum, i, cycletime

        pronum += 1

    # probnum = 28
    # pronum = 1
    #
    # k = 0
    #
    # ka = KSP_ACTION()
    # ts = action.action()
    # sm = nextstate.simul()
    #
    # test = problemreader.ProblemReader(probnum)
    # rs = test.get_problem(pronum).rack.status
    # column = test.get_problem(pronum).rack.column
    # floor = test.get_problem(pronum).rack.floor
    # input = test.get_problem(pronum).input
    # output = test.get_problem(pronum).output
    #
    # rs0 = copy.deepcopy(rs)
    # rs1 = copy.deepcopy(rs)
    #
    # cycletime = 0
    # # size = len(input)/2
    # size = 10
    #
    # for cycle in range(size):
    #     inputs = input[(cycle+1)*2-2:(cycle+1)*2]
    #     outputs = output[(cycle+1)*2-2:(cycle+1)*2]
    #     a, b = ka.final_action_test(rs0, column, floor, inputs, outputs, k, 1)
    #     print
    #     print cycle, inputs, outputs
    #     print a.loc, a.type, b
    #     # a, b = ka.final_action_test(rs1, column, floor, inputs, outputs, k, 0)
    #     # print inputs, outputs
    #     # print a.loc, a.type, b
    #
    #     # sol, b = ka.select_action_considering_sr_shortest(rs,column,floor,inputs,outputs,k)
    #     rs0 = sm.change_rs(rs0, column, floor, a)
    #     cycletime += b
    # print pronum, cycletime

