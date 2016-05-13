from problemIO import problemreader
import action, reward, solution
import math


class ActionGenerator(object):

    def loca_calculate(self, index, size_h, size_v):

        loca = []

        if math.floor(index / (size_h * size_v)) == 0:
            loca.append(int(math.floor(index / (size_h * size_v))))
            loca.append(int(math.floor(index / size_v)))
            loca.append(int(index % size_v))

        else:
            loca.append(int(math.floor(index / (size_h * size_v))))
            loca.append(int(math.floor((index - size_h * size_v) / size_v)))
            loca.append(int((index - (size_h * size_v)) % size_v))

        return loca

    def change_to_two_dimension1(self, rack_status, columnNum, floorNum):
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[row * floorNum + col]
        return result

    def change_to_two_dimension2(self, rack_status, columnNum, floorNum):
        result = [[0.0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[columnNum * floorNum + row * floorNum + col]
        return result

    def right_search(self, rack, column, floor, sol, idx):
        # rightward direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []
        max_col = column - 1
        max_flo = floor - 1
        dif_col = max_col - target_loc[1]
        dif_flo = max_flo - target_loc[2]
        upper_slope = float(dif_flo) / dif_col
        lower_slope = float(-target_loc[2]) / dif_col

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1]:
                    if loca1[2] == target_loc[2]:
                        lot.append(loca1)
                    elif loca1[2] > target_loc[2]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if target_slope < upper_slope:
                            lot.append(loca1)
                    elif loca1[2] < target_loc[2]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if lower_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def left_search(self, rack, column, floor, sol, idx):
        # leftward direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []
        max_flo = floor - 1
        dif_col = - target_loc[1]
        dif_flo = max_flo - target_loc[2]
        upper_slope = float(dif_flo) / dif_col
        lower_slope = float(-target_loc[2]) / dif_col

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1]:
                    if loca1[2] == target_loc[2]:
                        lot.append(loca1)
                    elif loca1[2] > target_loc[2]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if upper_slope < target_slope:
                            lot.append(loca1)
                    elif loca1[2] < target_loc[2]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if lower_slope > target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def top_search(self, rack, column, floor, sol, idx):
        # top direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []
        max_col = column - 1
        max_flo = floor - 1
        dif_col = max_col - target_loc[1]
        dif_flo = max_flo - target_loc[2]
        right_slope = float(dif_flo) / dif_col
        left_slope = float(dif_flo) / (- target_loc[1])

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] > target_loc[2]:
                    if loca1[1] == target_loc[1]:
                        lot.append(loca1)
                    elif loca1[1] > target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if target_slope > right_slope:
                            lot.append(loca1)
                    elif loca1[1] < target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if left_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def bottom_search(self, rack, column, floor, sol, idx):
        # bottom direction search

        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []
        max_col = column - 1
        dif_col = max_col - target_loc[1]
        right_slope = float(- target_loc[2]) / dif_col
        left_slope = float(- target_loc[2]) / (- target_loc[1])

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] < target_loc[2]:
                    if loca1[1] == target_loc[1]:
                        lot.append(loca1)
                    elif loca1[1] > target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if target_slope > right_slope:
                            lot.append(loca1)
                    elif loca1[1] < target_loc[1]:
                        target_slope = float((loca1[2] - target_loc[2])) / (loca1[1] - target_loc[1])
                        if left_slope < target_slope:
                            lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def right_top_search(self, rack, column, floor, sol, idx):
        # upper right search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1] and loca1[2] > target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def right_bottom_search(self, rack, column, floor, sol, idx):
        # below right search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target_loc[1] and loca1[2] < target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def left_top_search(self, rack, column, floor, sol, idx):
        # upper left search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1] and loca1[2] > target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def left_bottom_search(self, rack, column, floor, sol, idx):
        # below left search
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target_loc[1] and loca1[2] < target_loc[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def before_search(self, rack, column, floor, sol, idx):
        # close to after point
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        if idx == 0:
            before_node = [0, 0, 0]
        else:
            before_node = sol.loc[idx - 1]

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if min(target_loc[1], before_node[1]) < loca1[1] < max(target_loc[1], before_node[1]) \
                        and min(target_loc[2], before_node[2]) < loca1[2] < max(target_loc[2], before_node[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target_loc[1]), 2) + math.pow((lot[b][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def next_search(self, rack, column, floor, sol, idx):
        # close to after point
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            target_num = target_type

        lot = []

        if idx == 3:
            next_node = [0, 0, 0]
        else:
            next_node = sol.loc[idx + 1]

        for a, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(a, column, floor)
                if min(target_loc[1], next_node[1]) < loca1[1] < max(target_loc[1], next_node[1]) \
                        and min(target_loc[2], next_node[2]) < loca1[2] < max(target_loc[2], next_node[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1]-target_loc[1]), 2) + math.pow((lot[b][2]-target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[b]
                    distance = new_distance
            return sol

    def item_search(self, rack, column, floor, sol, idx):
        # close to median value of the item
        target_loc = sol.loc[idx]
        target_seq = sol.oper[idx]
        # target_type = sol.type[idx]

        if target_seq == 'S' or target_seq == 's':
            target_num = -1
        elif target_seq == 'R' or target_seq == 'r':
            return sol

        lot = []
        sublot = []

        for a, item1 in enumerate(rack):
            if item1 == sol.type[idx]:
                loca1 = self.loca_calculate(a, column, floor)
                sublot.append(loca1)

        target_to = [0, 0, 0]
        target_to_go = [0, 0, 0]

        for b in range(len(sublot)):
            target_to[1] += sublot[b][1]
            target_to[2] += sublot[b][2]

        target_to_go[1] = float(target_to[1]) / len(sublot)
        target_to_go[2] = float(target_to[2]) / len(sublot)

        for c, item1 in enumerate(rack):
            if item1 == target_num:
                loca1 = self.loca_calculate(c, column, floor)
                if min(target_loc[1], target_to_go[1]) < loca1[1] < max(target_loc[1], target_to_go[1]) \
                        and min(target_loc[2], target_to_go[2]) < loca1[2] < max(target_loc[2], target_to_go[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - target_loc[1]), 2) + math.pow((lot[d][2] - target_loc[2]), 2)
                if distance > new_distance:
                    sol.loc[idx] = lot[d]
                    distance = new_distance
            return sol

    def generating_idx(self, rack, column, floor, sol, idx, iter):
        # idx means action type
        # iter means operate time
        cal = reward.reward()

        if idx == 0:
            cycletime = cal.get_cycletime(sol)
            return sol, cycletime

        elif idx == 1:
            new_sol = self.right_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 2:
            new_sol = self.left_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 3:
            new_sol = self.top_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 4:
            new_sol = self.bottom_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 5:
            new_sol = self.right_top_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 6:
            new_sol = self.right_bottom_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 7:
            new_sol = self.left_top_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 8:
            new_sol = self.left_bottom_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 9:
            new_sol = self.before_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 10:
            new_sol = self.next_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 11:
            new_sol = self.item_search(rack, column, floor, sol, iter)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

if __name__ == '__main__':

    test = problemreader.ProblemReader(10)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    make = ActionGenerator()
    # for a in range(floor):
    #    print (floor - a - 1), make.change_to_two_dimension1(rs, column, floor)[floor - a - 1], '    ', \
    #        make.change_to_two_dimension2(rs, column, floor)[floor - 1 - a]

    ts = action.action()
    sol = ts.dijk(rs, column, floor, [664, 277], [84, 753])[0]
    print column, floor, sol.type, sol.oper, sol.loc

    # S1 has 10 actions
    # R2 has 9 actions

    # for i in range(0, 8):
    #    new_sol = sol
    #    print make.s1_generating_idx(rs, column, floor, new_sol, i)[0].loc, make.s1_generating_idx(rs, column, floor, new_sol, i)[1]

    print make.before_search(rs, column, floor, sol, 0).loc
    print make.before_search(rs, column, floor, sol, 1).loc
    print make.before_search(rs, column, floor, sol, 2).loc
    print make.before_search(rs, column, floor, sol, 3).loc