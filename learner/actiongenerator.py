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

    def right_greedy_search(self, rack, column, floor, sol):
        # leftward direction search

        # sol.type = [[1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 4, 1]]
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
            sol.loc[0] = lot[0]
            return sol

    def left_greedy_search(self, rack, column, floor, sol):
        # leftward direction search

        # sol.type = [[1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 4, 1]]
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
            lot.reverse()
            sol.loc[0] = lot[0]
            return sol

    def top_greedy_search(self, rack, column, floor, sol):
        # leftward direction search

        # sol.type = [[1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 4, 1]]
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
            sol.loc[0] = lot[0]
            return sol

    def bottom_greedy_search(self, rack, column, floor, sol):
        # leftward direction search

        # sol.type = [[1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 4, 1]]
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
            lot.reverse()
            sol.loc[0] = lot[0]
            return sol

    def generating_idx(self, rack, column, floor, sol, idx):
        cal = reward.reward()
        if idx == 0:
            cycletime = cal.get_cycletime(sol)
            return sol, cycletime

        elif idx == 1:
            new_sol = self.right_greedy_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 2:
            new_sol = self.left_greedy_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 3:
            new_sol = self.top_greedy_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

        elif idx == 4:
            new_sol = self.bottom_greedy_search(rack, column, floor, sol)
            cycletime = cal.get_cycletime(new_sol)
            return new_sol, cycletime

    def io_partial_search(self, rack, column, floor, sol):
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
                new_distance = math.sqrt(lot[b][1]-0) + math.sqrt(lot[b][2]-0)
                if distance < new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance

            return sol

    def next_partial_search(self, rack, column, floor, sol):
        # close to after point
        target = sol.loc[0]
        next_node = sol.loc[1]
        lot = []

        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, column, floor)
                if target[1] < loca1[1] < next_node[1] and target[2] < loca1[2] < next_node[2]:
                    lot.append(loca1)

        if lot == []:
            return sol
        else:
            distance = 10000
            for b in range(len(lot)):
                new_distance = math.sqrt(lot[b][1]-target[1]) + math.sqrt(lot[b][2]-target[2])
                if distance > new_distance:
                    sol.loc[0] = lot[b]
                    distance = new_distance

            return sol

    def full_search(self, rack, column, floor, sol):
        # close to median value of the item
        return

if __name__ == '__main__':

    test = problemreader.ProblemReader(20)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    make = ActionGenerator()
    for a in range(floor):
        print make.change_to_two_dimension1(rs, column, floor)[a], '    ', make.change_to_two_dimension2(rs, column, floor)[a]

    ts = action.action()
    sol = ts.dijk(rs, column, floor, [700, 392], [24, 24])[0]
    print sol.type, sol.oper, sol.loc

    print make.next_partial_search(rs, column, floor, sol).loc
    # for i in range(0, 5):
    #    print make.generating_idx(rs, column, floor, sol, i)[0].loc, make.generating_idx(rs, column, floor, sol, i)[1]
