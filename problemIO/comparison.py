from problemIO import problemreader
from simulator import nextstate
from learner import action
import time
import copy


def dijk(test_data):
    for problem_set in test_data:
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

            at = action.action()
            start = time.time()
            solution,cycletime = at.dijk(rack, clm, flr, input, output)

            end = time.time()
            sim = nextstate.simul()

            rack = sim.change_rs(rack, clm, flr, solution)

            elapsed = end - start
            total_cycletime += cycletime
            total_elapsed += elapsed

        print total_cycletime
        print total_elapsed

if __name__ == '__main__':
    pr2 = problemreader.ProblemReader(25)
    dijk(pr2.get_problems(10))