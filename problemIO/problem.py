class Problem:

    def __init__(self, aisleNum, columnNum, floorNum, itemTypeNum, shuttleNum):
        self.aisleNum = aisleNum
        self.columnNum = columnNum
        self.floorNum = floorNum
        self.itemTypeNum = itemTypeNum
        self.shuttleNum = shuttleNum

    def set_problem(self, rack, input, output):
        self.rack = rack
        self.input = input
        self.output = output

class ProblemWithSolution(Problem):

    def set_problem_with_solution(self, rack, input, output, NN_sol, RNN_sol):
        self.rack = rack
        self.input = input
        self.output = output
        self.NN_sol = NN_sol
        self.RNN_sol = RNN_sol