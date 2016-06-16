from problemIO import problemreader
from simulator import nextstate
from learner import action
import time
import copy


def dijk(test_data):

    cnt = 0

    for problem_set in test_data:

        cnt += 1
        if cnt == 1 or cnt == 2:
            continue

        total_cycletime = 0.0

        sht = problem_set.shuttleNum
        clm = problem_set.columnNum
        flr = problem_set.floorNum

        rack = copy.deepcopy(problem_set.rack.status)

        cycleNum = problem_set.requestLength / sht

        total_elapsed = 0.0

        for order_idx in range(cycleNum):
            input = problem_set.input[order_idx * sht:order_idx * sht + sht]
            output = problem_set.output[order_idx * sht:order_idx * sht + sht]

            ##if output[0] > output[1]:
            ##    output.reverse()

            at = action.action()
            start = time.time()

            print order_idx, total_cycletime, input, output, rack
            solution,cycletime = at.dijk(rack, clm, flr, input, output)

            end = time.time()
            sim = nextstate.simul()

            rack = sim.change_rs(rack, clm, flr, solution)

            elapsed = end - start
            total_cycletime += cycletime
            total_elapsed += elapsed



if __name__ == '__main__':
    pr2 = problemreader.ProblemReader(28)
    dijk(pr2.get_problems(10))

