from problemIO import problemreader
from simulator import nextstate
from learner import action


def dijk(test_data):
    for problem_set in test_data:
        total_cycletime = 0.0

        sht = problem_set.shuttleNum
        clm = problem_set.columnNum
        flr = problem_set.floorNum

        rack = problem_set.rack.status

        cycleNum = problem_set.requestLength / sht

        for order_idx in range(cycleNum):
            input = problem_set.input[order_idx * sht:order_idx * sht + sht]
            output = problem_set.output[order_idx * sht:order_idx * sht + sht]

            at = action.action()
            solution, cycletime = at.dijk_idx(rack, clm, flr, input, output, 0)

            sim = nextstate.simul()

            rack = sim.change_rs(rack, clm, flr, solution)

            total_cycletime += cycletime
        print total_cycletime


if __name__ == '__main__':
    pr2 = problemreader.ProblemReader(20)
    dijk(pr2.get_problems(3))