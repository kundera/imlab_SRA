import matplotlib.pyplot as plt
import math
from problemIO import problemreader


class visualize():

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

    def visual_rack(self, rack, column, floor):

        rs1 = []
        rs11 = []
        rs2 = []
        rs22 = []

        for a in range(len(rack)/2):
            rs1.append(self.loca_calculate(a, column, floor)[1:3])
            if rack[a] == -1:
                rs11.append('r')
            else:
                rs11.append(str(1-rack[a] / 25.))

            rs2.append(self.loca_calculate((len(rack)/2)+a, column, floor)[1:3])
            if rack[len(rack) / 2 + a] == -1:
                rs22.append('r')
            else:
                rs22.append(str(1-rack[(len(rack)/2)+a] / 25.))

        plt.figure(figsize=(column/2, floor/4))

        plt.axis([-1, column*2, -1, floor])
        for a in range(len(rack)/2):
            plt.scatter(rs1[a][0]*2, rs1[a][1], s=200, marker='s', c=rs11[a])
            plt.scatter(rs2[a][0]*2+1, rs2[a][1], s=200, marker='s', c=rs22[a])
        plt.show()

if __name__ == '__main__':

    test = problemreader.ProblemReader(25)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor
    # print rs
    ts = visualize()
    ts.visual_rack(rs, column, floor)

    print 'end'