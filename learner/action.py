from simulator import Simulator
from problemIO import problemreader
import networkx as nx
import math
import matplotlib.pyplot as plt

class action(object):

    tidx = 6 # tableidx in DB
    pidx = 1 # problemidx in DB
    testset = problemreader.ProblemWithSolutionReader(tidx, pidx) # get test set from DB
    rs1 = testset.get_problem_with_solution().rack
    rack_size_h = testset.get_problem_with_solution().columnNum # the number of column
    rack_size_v = testset.get_problem_with_solution().floorNum # the number of floor
    input = testset.get_problem_with_solution().input
    output = testset.get_problem_with_solution().output
    input_list = input.replace(" ","").split(",")
    output_list = output.replace(" ","").split(",")
    yspeed = 2.5
    zspeed = 0.6666667


    simul = Simulator.simul()

    def loca_calculate(self, index):

        loca = []

        if index / (action.rack_size_h * action.rack_size_v) == 0 :
            loca.append(int(math.floor(index / (action.rack_size_h * action.rack_size_v))))
            loca.append(int(math.floor(index / action.rack_size_v)))
            loca.append(int(index % action.rack_size_v))

        else :
            loca.append(int(math.floor(index / (action.rack_size_h * action.rack_size_v))))
            loca.append(int(math.floor((index - action.rack_size_h * action.rack_size_v) / action.rack_size_v)))
            loca.append(int((index - (action.rack_size_h * action.rack_size_v)) % action.rack_size_v))

        return loca


    def get_time(self, start, end):

        return max(abs((start[1] - end[1]) / self.yspeed),
                   abs((start[2] - end[2]) / self.zspeed))


    def dijk_ssrr(self, rs):
        G = nx.Graph()
        G.add_node('start',loca=[0,0,0])
        G.add_node('end',loca=[0,0,0])
        rack = action.simul.adjust_rs(rs)
        init_loca = [0,0,0]
        end_loca = [0,0,0]
# ============================================== create first 'S'=======================================================
        for a, item in enumerate(rack):
            if item == -1 :
                loca1 = self.loca_calculate(a)
                print loca1
                #minus_one_list = []
                #minus_one_list.append(item)
                #for i in
                G.add_node('%s_s1'%(a),loca=loca1)
                G.add_edge('start', '%s_s1'%(a), weight = self.get_time(init_loca,loca1))
                #G.add_
#============================================== create second 'S'=======================================================

                for b, item in enumerate(rack):
                    if item == -1 :
                        loca2 = self.loca_calculate(b)
                        G.add_node('%s_s2'%(b),loca=loca2)
                        G.add_edge('%s_s1'%(a), '%s_s2'%(b), weight = self.get_time(loca1,loca2))

#============================================== remove edges weighted 0=================================================
                        for n,nbrs in G.adjacency_iter():
                            for nbr,eattr in nbrs.items():
                                data = eattr['weight']
                                if data == 0.0:
                                    G.remove_edge('%s'%(n), '%s'%(nbr))

# ============================================== create first 'R'=======================================================

        print G.node
        print G.edge
        print input
        nx.draw_networkx(G ,arrows=True,with_labels=True)
        plt.show()


test = action()
rs1 = test.rs1

print test.dijk_ssrr(rs1)

