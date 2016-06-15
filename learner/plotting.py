from problemIO import problemreader
import math
import copy
import action
from simulator import nextstate
from simulator import visualize_rack

import matplotlib.pyplot as plt


class graph():

    def cycle_gragh(self):

        return

if __name__ == '__main__':
    probnum = 28
    pronum = 1

    test = problemreader.ProblemReader(probnum)
    rs = test.get_problem(pronum).rack.status
    column = test.get_problem(pronum).rack.column
    floor = test.get_problem(pronum).rack.floor
    input = test.get_problem(pronum).input
    output = test.get_problem(pronum).output

    ts = action.action()
    sm = nextstate.simul()

    size = len(input) / 2

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # rs0 = copy.deepcopy(rs)
    # rs1 = copy.deepcopy(rs)
    rs2 = copy.deepcopy(rs)
    rs3 = copy.deepcopy(rs)
    rs4 = copy.deepcopy(rs)
    rs5 = copy.deepcopy(rs)
    rs6 = copy.deepcopy(rs)
    rs7 = copy.deepcopy(rs)

    cycletime0 = 0
    cycletime1 = 0
    cycletime2 = 0
    cycletime3 = 0
    cycletime4 = 0
    cycletime5 = 0
    cycletime6 = 0
    cycletime7 = 0
    #
    # temp1 = 0
    # temp2 = 0
    # temp3 = 0
    #
    # for i1 in range(len(rs2)):
    #     if rs2[i1] == 3:
    #         temp1 += 1

    for i in range(size):
        # temp4 = 0
        # temp5 = 0
        inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]

        # print inputs
        # print outputs
        # if inputs[0] == 3:
        #     temp2 += 1
        # if inputs[1] == 3:
        #     temp2 += 1
        # if outputs[0] == 3:
        #     temp3 += 1
        # if outputs[1] == 3:
        #     temp3 += 1
        # for tb in range(len(rs0)):
        #     if rs0[tb] == 3:
        #         temp5 += 1
        # for ta in range(len(rs2)):
        #     if rs2[ta] == 3:
        #         temp4 += 1
        # print temp5, temp4
        # print temp2, temp3
        # print rs0
        # print rs2

        # a, b = ts.dijk_srsr_with_abc_a(rs0, column, floor, inputs, outputs)
        # c, d = ts.dijk_srsr_with_abc_b(rs1, column, floor, inputs, outputs)
        e, f = ts.dijk_srsr_faster_one(rs2, column, floor, inputs, outputs)
        g, h = ts.dijk_srsr_density_test_fixed_output(rs3, column, floor, inputs, outputs)
        t, j = ts.dijk_srsr_density(rs4, column, floor, inputs, outputs, 0)
        l, m = ts.dijk_srsr_density(rs5, column, floor, inputs, outputs, 1)
        n, o = ts.dijk_srsr_density(rs6, column, floor, inputs, outputs, 2)
        p, q = ts.dijk_srsr_density(rs7, column, floor, inputs, outputs, 3)

        # cycletime0 += b
        # cycletime1 += d
        cycletime2 += f
        cycletime3 += h
        cycletime4 += j
        cycletime5 += m
        cycletime6 += o
        cycletime7 += q

        # rs0 = sm.change_rs(rs0, column, floor, a)
        # rs1 = sm.change_rs(rs1, column, floor, c)
        rs2 = sm.change_rs(rs2, column, floor, e)
        rs3 = sm.change_rs(rs3, column, floor, g)
        rs4 = sm.change_rs(rs4, column, floor, t)
        rs5 = sm.change_rs(rs5, column, floor, l)
        rs6 = sm.change_rs(rs6, column, floor, n)
        rs7 = sm.change_rs(rs7, column, floor, p)
        # print rs0


        # plt.scatter(i, cycletime0, s=2, color='b')
        # plt.scatter(i, cycletime1, s=2, color='g')
        ax.scatter(i, cycletime2, s=2, color='r')
        ax.scatter(i, cycletime3, s=2, color='c')
        ax.scatter(i, cycletime4, s=2, color='m')
        ax.scatter(i, cycletime5, s=2, color='y')
        ax.scatter(i, cycletime6, s=2, color='k')
        ax.scatter(i, cycletime7, s=2, color='g')


        print i
        print '-------------------------'

    ax.annotate('red = faster one', xy=(300, 1000))
    ax.annotate('cyan = density test fixed', xy=(300, 900))
    ax.annotate('magenta = dijk density 0', xy=(300, 800))
    ax.annotate('yellow = dijk density 1', xy=(300, 700))
    ax.annotate('black = dijk density 2', xy=(300, 600))
    ax.annotate('green = dijk density 3', xy=(300, 500))
    plt.show()