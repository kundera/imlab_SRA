import ksp
import action
from problemIO import problemreader
from simulator import nextstate

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
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

                return sol, cycletime

            elif input[0] <= input[1] and output[1] < output[0]:
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                sol, cycletime = self.select_action_considering_sr_shortest(rs, column, floor, input, output, k)

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


if __name__ == '__main__':

    probnum = 28
    pronum = 2

    k = 1

    ka = KSP_ACTION()
    ts = action.action()
    sm = nextstate.simul()


    while pronum < 6:

        for i in range(0,17):
            test = problemreader.ProblemReader(probnum)
            rs = test.get_problem(pronum).rack.status
            column = test.get_problem(pronum).rack.column
            floor = test.get_problem(pronum).rack.floor
            input = test.get_problem(pronum).input
            output = test.get_problem(pronum).output
            cycletime = 0

            for cycle in range(len(input)/2):
                inputs = input[(cycle+1)*2-2:(cycle+1)*2]
                outputs = output[(cycle + 1) * 2 - 2:(cycle + 1) * 2]
                sol, b = ka.actions_test(rs,column,floor,inputs,outputs,k,i)
                rs = sm.change_rs(rs, column, floor, sol)
                cycletime += b
            print pronum, i, cycletime

        pronum += 1

    # probnum = 28
    # pronum = 2
    #
    # k = 1
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
    # cycletime = 0
    #
    # for cycle in range(len(input)/2):
    #     inputs = input[(cycle+1)*2-2:(cycle+1)*2]
    #     outputs = output[(cycle+1)*2-2:(cycle+1)*2]
    #     sol, b = ka.select_action_considering_sr_shortest(rs,column,floor,inputs,outputs,k)
    #     rs = sm.change_rs(rs, column, floor, sol)
    #     cycletime += b
    # print pronum, cycletime

