from problemIO import problemreader
import math
import solution
import time


class heuristics(object):
    ySpeed = 2.5
    zSpeed = 0.6666667

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

    def get_cycletime(self, solution):
        cycletime = 0.0
        for i in range(len(solution.loc)):
            if i == 0:
                cycletime += self.get_time([0, 0, 0], solution.loc[i])
            else:
                cycletime += self.get_time(solution.loc[i], solution.loc[i - 1])

        cycletime += self.get_time([0, 0, 0], solution.loc[len(solution.loc) - 1])
        return cycletime

    def get_time(self, start, end):
        return max(abs((float(start[1]) - float(end[1])) / self.ySpeed),
                   abs((float(start[2]) - float(end[2])) / self.zSpeed))

    def nearest_neighbor_s1s2r1r2(self, rs, column, floor, input, output):

        rack = rs
        size_h = column
        size_v = floor

        s1 = input[0]
        s2 = input[1]
        r1 = output[0]
        r2 = output[1]
        item = [s1, s2, r1, r2]
        io = ['s1', 's2', 'r1', 'r2']

        path = ['first', 'second', 'third', 'fourth']

        # s1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - 0), 2) + math.pow((lot[b][2] - 0), 2)
                if distance > new_distance:
                    path[0] = lot[b]
                    distance = new_distance

        # s2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - path[0][1]), 2) + math.pow((lot[d][2] - path[0][2]), 2)
                if distance > new_distance and path[0] != lot[d]:
                    path[1] = lot[d]
                    distance = new_distance

        # r1
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == r1:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = math.pow((lot[f][1] - path[1][1]), 2) + math.pow((lot[f][2] - path[1][2]), 2)
                if distance > new_distance:
                    path[2] = lot[f]
                    distance = new_distance

        # r2
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == r2:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = math.pow((lot[h][1] - path[2][1]), 2) + math.pow((lot[h][2] - path[2][2]), 2)
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        return sol, cycletime

    def nearest_neighbor_s1s2r2r1(self, rs, column, floor, input, output):

        rack = rs
        size_h = column
        size_v = floor

        s1 = input[0]
        s2 = input[1]
        r1 = output[0]
        r2 = output[1]
        item = [s1, s2, r2, r1]
        io = ['s1', 's2', 'r2', 'r1']

        path = ['first', 'second', 'third', 'fourth']

        # s1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - 0), 2) + math.pow((lot[b][2] - 0), 2)
                if distance > new_distance:
                    path[0] = lot[b]
                    distance = new_distance

        # s2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - path[0][1]), 2) + math.pow((lot[d][2] - path[0][2]), 2)
                if distance > new_distance and path[0] != lot[d]:
                    path[1] = lot[d]
                    distance = new_distance

        # r2
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == r2:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = math.pow((lot[f][1] - path[1][1]), 2) + math.pow((lot[f][2] - path[1][2]), 2)
                if distance > new_distance:
                    path[2] = lot[f]
                    distance = new_distance

        # r1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == r1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = math.pow((lot[h][1] - path[2][1]), 2) + math.pow((lot[h][2] - path[2][2]), 2)
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        return sol, cycletime

    def nearest_neighbor_s1r1s2r2(self, rs, column, floor, input, output):

        rack = rs
        size_h = column
        size_v = floor

        s1 = input[0]
        s2 = input[1]
        r1 = output[0]
        r2 = output[1]
        item = [s1, r1, s2, r2]
        io = ['s1', 'r1', 's2', 'r2']

        path = ['first', 'second', 'third', 'fourth']

        # s1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - 0), 2) + math.pow((lot[b][2] - 0), 2)
                if distance > new_distance:
                    path[0] = lot[b]
                    distance = new_distance

        # r1
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == r1:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = math.pow((lot[f][1] - path[0][1]), 2) + math.pow((lot[f][2] - path[0][2]), 2)
                if distance > new_distance:
                    path[1] = lot[f]
                    path[2] = lot[f]
                    distance = new_distance
        '''
        # s2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - path[1][1]), 2) + math.pow((lot[d][2] - path[1][2]), 2)
                if distance > new_distance and path[0] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance
        '''

        # r2
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == r2:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = math.pow((lot[h][1] - path[2][1]), 2) + math.pow((lot[h][2] - path[2][2]), 2)
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        return sol, cycletime

    def nearest_neighbor_s1r2s2r1(self, rs, column, floor, input, output):

        rack = rs
        size_h = column
        size_v = floor

        s1 = input[0]
        s2 = input[1]
        r1 = output[0]
        r2 = output[1]
        item = [s1, r2, s2, r1]
        io = ['s1', 'r2', 's2', 'r1']

        path = ['first', 'second', 'third', 'fourth']

        # s1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = math.pow((lot[b][1] - 0), 2) + math.pow((lot[b][2] - 0), 2)
                if distance > new_distance:
                    path[0] = lot[b]
                    distance = new_distance

        # r2
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == r2:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = math.pow((lot[f][1] - path[0][1]), 2) + math.pow((lot[f][2] - path[0][2]), 2)
                if distance > new_distance:
                    path[1] = lot[f]
                    path[2] = lot[f]
                    distance = new_distance
        '''
        # s2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = math.pow((lot[d][1] - path[1][1]), 2) + math.pow((lot[d][2] - path[1][2]), 2)
                if distance > new_distance and path[0] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance
        '''
        # r1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == r1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no target item'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = math.pow((lot[h][1] - path[2][1]), 2) + math.pow((lot[h][2] - path[2][2]), 2)
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        return sol, cycletime

    def nearest_idx(self, rs, column, floor, input, output, idx):

        if idx == 1:
            a = self.nearest_neighbor_s1s2r1r2(rs, column, floor, input, output)
            b = self.nearest_neighbor_s1s2r2r1(rs, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a
        elif idx == 2:
            a = self.nearest_neighbor_s1r1s2r2(rs, column, floor, input, output)
            b = self.nearest_neighbor_s1r2s2r1(rs, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a

if __name__ == '__main__':

    test = problemreader.ProblemReader(23)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    ts1 = heuristics()
    a = ts1.nearest_idx(rs, column, floor, [123, 456], [28, 29], 1)
    print a[0].loc, a[0].type, a[0].oper, a[1]

    a = ts1.nearest_idx(rs, column, floor, [123, 456], [28, 29], 2)
    print a[0].loc, a[0].type, a[0].oper, a[1]
