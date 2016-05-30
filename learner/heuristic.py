from problemIO import problemreader
import math
import solution
import copy
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
                new_distance = self.get_time([0, 0, 0], lot[b])
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
                new_distance = self.get_time(path[0], lot[d])
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
                new_distance = self.get_time(path[1], lot[f])
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
                new_distance = self.get_time(path[2], lot[h])
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
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
                new_distance = self.get_time([0, 0, 0], lot[b])
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
                new_distance = self.get_time(path[0], lot[d])
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
                new_distance = self.get_time(path[1], lot[f])
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
                new_distance = self.get_time(path[2], lot[h])
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
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
                new_distance = self.get_time([0, 0, 0], lot[b])
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
                new_distance = self.get_time(path[0], lot[f])
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
                new_distance = self.get_time(path[2], lot[h])
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
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
                new_distance = self.get_time([0, 0, 0], lot[b])
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
                new_distance = self.get_time(path[0], lot[f])
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
                new_distance = self.get_time(path[2], lot[h])
                if distance > new_distance and path[2] != lot[h]:
                    path[3] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
        return sol, cycletime

    def reverse_nearest_neighbor_s1s2r1r2(self, rs, column, floor, input, output):

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

        # r2
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == r2:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = self.get_time([0, 0, 0], lot[b])
                if distance > new_distance:
                    path[3] = lot[b]
                    distance = new_distance

        # r1
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == r1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = self.get_time(path[3], lot[d])
                if distance > new_distance and path[3] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance

        # s2
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == -1:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = self.get_time(path[2], lot[f])
                if distance > new_distance:
                    path[1] = lot[f]
                    distance = new_distance

        # s1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == -1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = self.get_time(path[1], lot[h])
                if distance > new_distance and path[1] != lot[h]:
                    path[0] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
        return sol, cycletime

    def reverse_nearest_neighbor_s1s2r2r1(self, rs, column, floor, input, output):

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

        # r1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == r1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = self.get_time([0, 0, 0], lot[b])
                if distance > new_distance:
                    path[3] = lot[b]
                    distance = new_distance

        # r2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == r2:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = self.get_time(path[3], lot[d])
                if distance > new_distance and path[3] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance

        # s2
        lot = []
        for e, item3 in enumerate(rack):
            if item3 == -1:
                loca3 = self.loca_calculate(e, size_h, size_v)
                lot.append(loca3)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for f in range(len(lot)):
                new_distance = self.get_time(path[2], lot[f])
                if distance > new_distance:
                    path[1] = lot[f]
                    distance = new_distance

        # s1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == -1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = self.get_time(path[1], lot[h])
                if distance > new_distance and path[1] != lot[h]:
                    path[0] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
        return sol, cycletime

    def reverse_nearest_neighbor_s1r1s2r2(self, rs, column, floor, input, output):

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

        # r2
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == r2:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = self.get_time([0, 0, 0], lot[b])
                if distance > new_distance:
                    path[3] = lot[b]
                    distance = new_distance

        # r1
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == r1:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = self.get_time(path[3], lot[d])
                if distance > new_distance and path[3] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance
                    # s2
                    path[1] = lot[d]
        # s1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == -1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = self.get_time(path[1], lot[h])
                if distance > new_distance and path[1] != lot[h]:
                    path[0] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
        return sol, cycletime

    def reverse_nearest_neighbor_s1r2s2r1(self, rs, column, floor, input, output):

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

        # r1
        lot = []
        for a, item1 in enumerate(rack):
            if item1 == r1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot.append(loca1)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for b in range(len(lot)):
                new_distance = self.get_time([0, 0, 0], lot[b])
                if distance > new_distance:
                    path[3] = lot[b]
                    distance = new_distance

        # r2
        lot = []
        for c, item2 in enumerate(rack):
            if item2 == r2:
                loca2 = self.loca_calculate(c, size_h, size_v)
                lot.append(loca2)

        if lot == []:
            print 'no item'
        else:
            distance = 10000
            lot.sort()
            for d in range(len(lot)):
                new_distance = self.get_time(path[3], lot[d])
                if distance > new_distance and path[3] != lot[d]:
                    path[2] = lot[d]
                    distance = new_distance
                    # s2
                    path[1] = lot[d]
        # s1
        lot = []
        for g, item4 in enumerate(rack):
            if item4 == -1:
                loca4 = self.loca_calculate(g, size_h, size_v)
                lot.append(loca4)

        if lot == []:
            print 'no empty space'
        else:
            distance = 10000
            lot.sort()
            for h in range(len(lot)):
                new_distance = self.get_time(path[1], lot[h])
                if distance > new_distance and path[1] != lot[h]:
                    path[0] = lot[h]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)
        # print path, item, io, cycletime
        return sol, cycletime

    def shortest_path(self, rs, column, floor, input, output):
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

        # s1 - r1
        lot1 = []
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                lot1.append(loca1)

        if lot1 == []:
            print 'no empty space'
        else:
            lot2 = []
            for b, item3 in enumerate(rack):
                if item3 == r1:
                    loca3 = self.loca_calculate(b, size_h, size_v)
                    lot2.append(loca3)

            if lot2 == []:
                print 'no target item'
            else:
                distance = 10000
                lot1.sort()
                lot2.sort()
                for c in range(len(lot1)):
                    for d in range(len(lot2)):
                        new_distance = self.get_time([0, 0, 0], lot1[c]) + self.get_time(lot1[c], lot2[d])
                        if distance > new_distance:
                            path[0] = lot1[c]
                            path[1] = lot2[d]
                            distance = new_distance
                            # s2
                            path[2] = lot2[d]
        # r2
        lot3 = []
        for e, item4 in enumerate(rack):
            if item4 == r2:
                loca4 = self.loca_calculate(e, size_h, size_v)
                lot3.append(loca4)

        if lot3 == []:
            print 'no target item'
        else:
            distance = 10000
            lot3.sort()
            for f in range(len(lot3)):
                new_distance = self.get_time([0, 0, 0], lot3[f]) + self.get_time(lot3[f], path[2])
                if distance > new_distance and path[2] != lot3[f]:
                    path[3] = lot3[f]
                    distance = new_distance

        sol = solution.solution(path, item, io)
        cycletime = self.get_cycletime(sol)

        return sol, cycletime

    def nearest_idx(self, rs, column, floor, input, output, idx):
        rack1 = copy.deepcopy(rs)
        rack2 = copy.deepcopy(rs)

        if idx == 0:
            a = self.nearest_neighbor_s1s2r1r2(rack1, column, floor, input, output)
            b = self.nearest_neighbor_s1s2r2r1(rack2, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a
        elif idx == 1:
            a = self.nearest_neighbor_s1r1s2r2(rack1, column, floor, input, output)
            b = self.nearest_neighbor_s1r2s2r1(rack2, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a

    def reverse_nearest_idx(self, rs, column, floor, input, output, idx):
        rack1 = copy.deepcopy(rs)
        rack2 = copy.deepcopy(rs)

        if idx == 0:  # ssrr
            a = self.reverse_nearest_neighbor_s1s2r1r2(rack1, column, floor, input, output)
            b = self.reverse_nearest_neighbor_s1s2r2r1(rack2, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a
        elif idx == 1:  # srsr
            a = self.reverse_nearest_neighbor_s1r1s2r2(rack1, column, floor, input, output)
            b = self.reverse_nearest_neighbor_s1r2s2r1(rack2, column, floor, input, output)
            if a[1] > b[1]:
                return b
            else:
                return a

    def nearest_density_idx(self, rs, column, floor, input, output, idx):
        rack1 = copy.deepcopy(rs)

        if idx == 0 or idx == 2 or idx == 4 or idx == 6:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[0], input[1]]
            else:
                input = [input[1], input[0]]
        elif idx == 1 or idx == 3 or idx == 5 or idx == 7:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[1], input[0]]
            else:
                input = [input[0], input[1]]

        if idx == 0 or idx == 1 or idx == 4 or idx == 5:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[0], output[1]]
            else:
                output = [output[1], output[0]]
        elif idx == 2 or idx == 3 or idx == 6 or idx == 7:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[1], output[0]]
            else:
                output = [output[0], output[1]]

        if 0 <= idx < 4:
            a = self.nearest_neighbor_s1s2r1r2(rack1, column, floor, input, output)
            return a
        elif 4 <= idx < 8:
            a = self.nearest_neighbor_s1r1s2r2(rack1, column, floor, input, output)
            return a

    def reverse_nearest_density_idx(self, rs, column, floor, input, output, idx):
        rack1 = copy.deepcopy(rs)

        if idx == 0 or idx == 2 or idx == 4 or idx == 6:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[0], input[1]]
            else:
                input = [input[1], input[0]]
        elif idx == 1 or idx == 3 or idx == 5 or idx == 7:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[1], input[0]]
            else:
                input = [input[0], input[1]]

        if idx == 0 or idx == 1 or idx == 4 or idx == 5:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[0], output[1]]
            else:
                output = [output[1], output[0]]
        elif idx == 2 or idx == 3 or idx == 6 or idx == 7:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[1], output[0]]
            else:
                output = [output[0], output[1]]

        if 0 <= idx < 4:  # ssrr
            a = self.reverse_nearest_neighbor_s1s2r1r2(rack1, column, floor, input, output)
            return a
        elif 4 <= idx < 8:  # srsr
            a = self.reverse_nearest_neighbor_s1r1s2r2(rack1, column, floor, input, output)
            return a

    def shortest_path_density_idx(self, rs, column, floor, input, output, idx):
        rack1 = copy.deepcopy(rs)
        # srsr
        # 0 - high low high low
        # 1 - low high high low
        # 2 - high low low high
        # 3 - low high low high

        if idx == 0 or idx == 2:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[0], input[1]]
            else:
                input = [input[1], input[0]]
        elif idx == 1 or idx == 3:
            if rs.count(input[0]) >= rs.count(input[1]):
                input = [input[1], input[0]]
            else:
                input = [input[0], input[1]]

        if idx == 0 or idx == 1:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[0], output[1]]
            else:
                output = [output[1], output[0]]
        elif idx == 2 or idx == 3:
            if rs.count(output[0]) >= rs.count(output[1]):
                output = [output[1], output[0]]
            else:
                output = [output[0], output[1]]

        a = self.shortest_path(rack1, column, floor, input, output)
        return a

if __name__ == '__main__':

    test = problemreader.ProblemReader(23)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor

    ts1 = heuristics()
    # a = ts1.shortest_path(rs, column, floor, [123, 456], [28, 29])
    # print a[0].loc, a[0].type, a[0].oper, a[1]
    print rs
    for b in range(4):
        a = ts1.shortest_path_density_idx(rs, column, floor, [22, 28], [27, 15], b)
        print a[0].loc, a[0].type, a[0].oper, a[1]
        print