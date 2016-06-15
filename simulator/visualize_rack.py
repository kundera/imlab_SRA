import matplotlib.pyplot as plt
import math
from problemIO import problemreader
import nextstate


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
                rs11.append(str(1 - rack[a] / 25.))

            rs2.append(self.loca_calculate((len(rack)/2)+a, column, floor)[1:3])
            if rack[len(rack) / 2 + a] == -1:
                rs22.append('r')
            else:
                rs22.append(str(1 - rack[(len(rack)/2) + a] / 25.))

        plt.figure(figsize=(column/2, floor/4))
        plt.axis([-1, column*2, -1, floor])

        for a in range(len(rack)/2):
            plt.scatter(rs1[a][0]*2, rs1[a][1], s=200, marker='s', color=rs11[a])
            plt.scatter(rs2[a][0]*2+1, rs2[a][1], s=200, marker='s', color=rs22[a])

        plt.show()

    def comparison_visual(self, rack, column, floor, i):

        plt.subplot(3, 3, i)

        rs1 = []
        rs11 = []
        rs2 = []
        rs22 = []

        for a in range(len(rack) / 2):
            rs1.append(self.loca_calculate(a, column, floor)[1:3])
            if rack[a] == -1:
                rs11.append('c')
            else:
                rs11.append(str(1 - rack[a] / 25.))

            rs2.append(self.loca_calculate((len(rack) / 2) + a, column, floor)[1:3])
            if rack[len(rack) / 2 + a] == -1:
                rs22.append('c')
            else:
                rs22.append(str(1 - rack[(len(rack) / 2) + a] / 25.))

        plt.axis([-1, column * 2, -1, floor])

        for a in range(len(rack) / 2):
            plt.scatter(rs1[a][0] * 2, rs1[a][1], s=200, marker='s', color=rs11[a])
            plt.scatter(rs2[a][0] * 2 + 1, rs2[a][1], s=200, marker='s', color=rs22[a])
        return

if __name__ == '__main__':

    test = problemreader.ProblemReader(25)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor
    input = test.get_problem(1).input
    output = test.get_problem(1).output

    vi = visualize()
    # vi.visual_rack(rs, column, floor)
    ts = action()
    sm = nextstate.simul()
    cycletime0 = 0

    rs0 = test.get_problem(2).rack.status

    for i in range(len(input) / 2):
        inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]

        a, b = ts.dijk_srsr_density(rs0, column, floor, inputs, outputs, 0)

        cycletime0 += b
        rs0 = sm.change_rs(rs0, column, floor, a)

        print a.type, a.loc

        if i % 10 == 0 and i != 0:
            vi.comparison_visual(rs0, column, floor, i/10)

        plt.show()