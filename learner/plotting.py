from problemIO import problemreader
import math
import copy
import action
import ksp_action
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
    ka = ksp_action.KSP_ACTION()
    sm = nextstate.simul()

    # size = len(input) / 2
    size = 500
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axes = plt.gca()
    axes.set_xlim([0, 500])
    axes.set_ylim([0, 4000])
    # size = 200
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # axes = plt.gca()
    # axes.set_xlim([0, 200])
    # axes.set_ylim([0, 2000])
    # size = 100
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # axes = plt.gca()
    # axes.set_xlim([0, 100])
    # axes.set_ylim([0, 1000])

    rs0 = copy.deepcopy(rs)
    rs1 = copy.deepcopy(rs)
    # rs2 = copy.deepcopy(rs)
    # rs3 = copy.deepcopy(rs)
    # rs4 = copy.deepcopy(rs)
    # rs5 = copy.deepcopy(rs)
    # rs6 = copy.deepcopy(rs)
    # rs7 = copy.deepcopy(rs)

    cycletime0 = 0
    cycletime1 = 0
    # cycletime2 = 0
    # cycletime3 = 0
    # cycletime4 = 0
    # cycletime5 = 0
    # cycletime6 = 0
    # cycletime7 = 0

    k = 0

    for i in range(size):

        inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]

        a, b = ka.final_action_test1(rs0, column, floor, inputs, outputs, k, 0)
        c, d = ka.final_action_test1(rs1, column, floor, inputs, outputs, k, 1)

        # a, b = ka.actions_test(rs0, column, floor, inputs, outputs, k, 2)
        # c, d = ka.actions_test(rs1, column, floor, inputs, outputs, k, 4)
        # e, f = ka.actions_test(rs2, column, floor, inputs, outputs, k, 10)
        # # g, h = ka.actions_test(rs3, column, floor, inputs, outputs, k, 10)
        # t, j = ka.actions_test(rs4, column, floor, inputs, outputs, k, 12)
        # l, m = ka.actions_test(rs5, column, floor, inputs, outputs, k, 14)
        # n, o = ts.dijk(rs6, column, floor, inputs, outputs)
        # p, q = ka.actions_test(rs7, column, floor, inputs, outputs, k, 16)

        # a, b = ts.dijk_srsr_with_abc_a(rs0, column, floor, inputs, outputs)
        # c, d = ts.dijk_srsr_with_abc_b(rs1, column, floor, inputs, outputs)
        # e, f = ts.dijk_srsr_faster_one(rs2, column, floor, inputs, outputs)
        # g, h = ts.dijk_srsr_density_test_fixed_output(rs3, column, floor, inputs, outputs)
        # t, j = ts.dijk_srsr_density(rs4, column, floor, inputs, outputs, 0)
        # l, m = ts.dijk_srsr_density(rs5, column, floor, inputs, outputs, 1)
        # n, o = ts.dijk_srsr_density(rs6, column, floor, inputs, outputs, 2)
        # p, q = ts.dijk_srsr_density(rs7, column, floor, inputs, outputs, 3)

        cycletime0 += b
        cycletime1 += d
        # cycletime2 += f
        # # cycletime3 += h
        # cycletime4 += j
        # cycletime5 += m
        # cycletime6 += o
        # cycletime7 += q

        rs0 = sm.change_rs(rs0, column, floor, a)
        rs1 = sm.change_rs(rs1, column, floor, c)
        # rs2 = sm.change_rs(rs2, column, floor, e)
        # # rs3 = sm.change_rs(rs3, column, floor, g)
        # rs4 = sm.change_rs(rs4, column, floor, t)
        # rs5 = sm.change_rs(rs5, column, floor, l)
        # rs6 = sm.change_rs(rs6, column, floor, n)
        # rs7 = sm.change_rs(rs7, column, floor, p)

        ax.scatter(i, cycletime0, s=10, color='b')
        ax.scatter(i, cycletime1, s=10, color='g')
        # ax.scatter(i, cycletime2, s=10, color='r')
        # # ax.scatter(i, cycletime3, s=2, color='c')
        # ax.scatter(i, cycletime4, s=10, color='m')
        # ax.scatter(i, cycletime5, s=10, color='y')
        # ax.scatter(i, cycletime6, s=10, color='k')
        # ax.scatter(i, cycletime7, s=10, color='0.5')
    #
        print i
        print '-------------------------'

    ax.annotate('blue = 0', xy=(90, 600))
    ax.annotate('green = 1', xy=(90, 500))
    plt.show()

    # # ax.annotate('blue = action 2', xy=(300, 1200))
    # # ax.annotate('green = action 4', xy=(300, 1100))
    # ax.annotate('red = action 10', xy=(150, 900))
    # # ax.annotate('cyan = action 10', xy=(300, 900))
    # ax.annotate('magenta = action 12', xy=(150, 800))
    # ax.annotate('yellow = action 14', xy=(150, 700))
    # ax.annotate('black = dijk', xy=(150, 600))
    # ax.annotate('gray = action 16', xy=(150, 500))
    # plt.show()

    # ax.annotate('blue = abc-a', xy=(300, 1200))
    # ax.annotate('green = abc-b', xy=(300, 1100))
    # ax.annotate('red = faster one', xy=(300, 1000))
    # ax.annotate('cyan = density test fixed', xy=(300, 900))
    # ax.annotate('magenta = dijk density 0', xy=(300, 800))
    # ax.annotate('yellow = dijk density 1', xy=(300, 700))
    # ax.annotate('black = dijk density 2', xy=(300, 600))
    # ax.annotate('white = dijk density 3', xy=(300, 500))
    # plt.show()