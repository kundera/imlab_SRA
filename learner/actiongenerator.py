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

    def s1_right_search(self, rack, column, floor, sol):
        # leftward direction search

        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] == target[2] and loca1[1] > target[1]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            itr = 10000
            for b in range(len(lot)):
                if itr > lot[b][1]:
                    sol.loc[0] = lot[b]
                    itr = lot[b][1]
            return sol

    def s1_left_search(self, rack, column, floor, sol):
        # leftward direction search

        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[2] == target[2] and loca1[1] < target[1]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            itr = 0
            for b in range(len(lot)):
                if itr < lot[b][1]:
                    sol.loc[0] = lot[b]
                    itr = lot[b][1]
            return sol

    def s1_top_search(self, rack, column, floor, sol):
        # leftward direction search

        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] == target[1] and loca1[2] > target[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            itr = 10000
            for b in range(len(lot)):
                if itr > lot[b][2]:
                    sol.loc[0] = lot[b]
                    itr = lot[b][2]
            return sol

    def s1_bottom_search(self, rack, column, floor, sol):
        # leftward direction search

        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] == target[1] and loca1[2] < target[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            itr = 0
            for b in range(len(lot)):
                if itr < lot[b][2]:
                    sol.loc[0] = lot[b]
                    itr = lot[b][2]
            return sol

    def s1_right_top_search(self, rack, column, floor, sol):
        # close to I/O point
        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target[1] and loca1[2] > target[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target[1]), 2) + math.pow((lot[b][2] - target[2]), 2)
                if distance > new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance
            return sol

    def s1_right_bottom_search(self, rack, column, floor, sol):
        # close to I/O point
        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] > target[1] and loca1[2] < target[2]:
                    lot.append(loca1)
                    print loca1

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target[1]), 2) + math.pow((lot[b][2] - target[2]), 2)
                if distance > new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance
            return sol

    def s1_left_top_search(self, rack, column, floor, sol):
        # close to I/O point
        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target[1] and loca1[2] > target[2]:
                    lot.append(loca1)
                    print loca1

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - target[1]), 2) + math.pow((lot[b][2] - target[2]), 2)
                if distance > new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance
            return sol

    def s1_left_bottom_search(self, rack, column, floor, sol):
        # close to I/O point
        target = sol.loc[0]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if loca1[1] < target[1] and loca1[2] < target[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 0
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1]-0), 2) + math.pow((lot[b][2]-0), 2)
                if distance < new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance

            return sol

    def s1_next_search(self, rack, column, floor, sol):
        # close to after point
        target = sol.loc[0]
        next_node = sol.loc[1]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if min(target[1], next_node[1]) < loca1[1] < max(target[1], next_node[1]) and \
                                        min(target[2], next_node[2]) < loca1[2] < max(target[2], next_node[2]):
                    lot.append(loca1)
                    print loca1

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1]-target[1]), 2) + math.pow((lot[b][2]-target[2]), 2)
                if distance > new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance

            return sol

    def s1_item_search(self, rack, column, floor, sol):
        # close to median value of the item
        target = sol.loc[0]
        lot = []
        sublot = []

        for a, item1 in enumerate(rack):
            if item1 == sol.type[0]:
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
            if item1 == -1:
                loca1 = self.loca_calculate(c, column, floor)
                if min(target[1], target_to_go[1]) < loca1[1] < max(target[1], target_to_go[1]) and \
                                        min(target[2], target_to_go[2]) < loca1[2] < max(target[2], target_to_go[2]):
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - target[1]), 2) + math.pow((lot[d][2] - target[2]), 2)
                if distance > new_distance:
                    sol.loc[0] = lot[d]
                    distance = new_distance
            return sol

    def generating_idx(self, rack, column, floor, sol, idx):
        cal = reward.reward()
        if idx == 0:
            cycletime = cal.get_cycletime(sol)
            return sol, cycletime

        elif idx == 1:
            new_sol = self.s1_right_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 2:
            new_sol = self.s1_left_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 3:
            new_sol = self.s1_top_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 4:
            new_sol = self.s1_bottom_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 5:
            new_sol = self.s1_right_top_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 6:
            new_sol = self.s1_right_bottom_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 7:
            new_sol = self.s1_left_top_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 8:
            new_sol = self.s1_left_bottom_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 9:
            new_sol = self.s1_next_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 10:
            new_sol = self.s1_item_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

if __name__ == '__main__':

    test = problemreader.ProblemReader(10)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    make = ActionGenerator()
    for a in range(floor):
        print make.change_to_two_dimension1(rs, column, floor)[floor - a - 1], '    ', make.change_to_two_dimension2(rs, column, floor)[floor - 1 - a]

    ts = action.action()
    sol = ts.dijk(rs, column, floor, [664, 277], [84, 760])[0]
    print sol.type, sol.oper, sol.loc

    #for i in range(0, 8):
    #    new_sol = sol
    #    print make.s1_generating_idx(rs, column, floor, new_sol, i)[0].loc, make.s1_generating_idx(rs, column, floor, new_sol, i)[1]

    # print make.s1_right_search(rs, column, floor, sol).loc
    # print make.s1_left_search(rs, column, floor, sol).loc
    # print make.s1_top_search(rs, column, floor, sol).loc
    # print make.s1_bottom_search(rs, column, floor, sol).loc
    # print make.s1_right_top_search(rs, column, floor, sol).loc
    # print make.s1_right_bottom_search(rs, column, floor, sol).loc
    print make.s1_left_top_search(rs, column, floor, sol).loc
    # print make.s1_left_bottom_search(rs, column, floor, sol).loc
    # print make.s1_next_search(rs, column, floor, sol).loc
    # print make.s1_item_search(rs, column, floor, sol).loc