from problemIO import problemreader
import action
import reward
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
            print lot
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


        return

    def partial_search(self, rack, column, floor, sol):
        # close to after point

        return

    def full_search(self, rack, column, floor, sol):
        # close to median value of the item
        return

if __name__ == '__main__':

    test = problemreader.ProblemReader(15)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    ts = action.action()
    sol = ts.dijk(rs, column, floor, [700, 392], [3, 0])[0]
    print sol.type, sol.oper, sol.loc

    make = ActionGenerator()

    print 1
    print make.left_greedy_search(rs, column, floor, sol).loc
    print 2
    print make.right_greedy_search(rs, column, floor, sol).loc
    print 3
    print make.top_greedy_search(rs, column, floor, sol).loc
    print 4
    print make.bottom_greedy_search(rs, column, floor, sol).loc
    print 5