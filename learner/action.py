from simulator import Simulator
from problemIO import problemreader
import networkx as nx
import math
import matplotlib.pyplot as plt

class action(object):

    tidx = 4 # tableidx in DB
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

        if math.floor(index / (action.rack_size_h * action.rack_size_v)) == 0 :
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


    def adjust_rs(self, rs1):
        rs1 = rs1.replace(" ", "")
        rs1 = rs1.split(",")

        return rs1

#=======================================================================================================================

    def dijk_ssr1r2(self, rs, output): # ex :output = raw data
        G = nx.Graph()
        G.add_node('start',loca=[0,0,0])
        G.add_node('end',loca=[0,0,0])
        rack = self.adjust_rs(rs)
        output_list = output.replace(" ", "").split(",")
        outputs = [output_list[i:i+2] for i in range(0, len(output_list), 2)]
        outputs = outputs[0]
        init_loca = [0,0,0]
        end_loca = [0,0,0]
# ============================================== create first 'S'=======================================================
        for a, item in enumerate(rack):
            if item == '-1' :
                loca1 = self.loca_calculate(a)
                #print loca1
                G.add_node('%s_s1'%(a),loca=loca1)
                G.add_edge('start', '%s_s1'%(a), weight = self.get_time(init_loca,loca1))

#============================================== create second 'S'=======================================================

                for b, item in enumerate(rack):
                    if item == '-1' :
                        loca2 = self.loca_calculate(b)
                        G.add_node('%s_s2'%(b),loca=loca2)
                        G.add_edge('%s_s1'%(a), '%s_s2'%(b), weight = self.get_time(loca1,loca2))

#============================================== remove edges weighted 0=================================================
                        for n,nbrs in G.adjacency_iter():
                            for nbr,eattr in nbrs.items():
                                data = eattr['weight']
                                if data == 0.0:
                                    G.remove_edge('%s'%(n), '%s'%(nbr))

# ============================================== create 'R1R2'============================================================

                        for c, item in enumerate(rack):
                            loca3 = self.loca_calculate(c)
                            if item == outputs[0]:
                                G.add_node('%s_r1' % (c), loca=loca3)
                                G.add_edge('%s_s2' % (b), '%s_r1' % (c), weight=self.get_time(loca2, loca3))

                                for d, item in enumerate(rack):
                                    loca4 = self.loca_calculate(d)
                                    if item == outputs[1]:
                                        G.add_node('%s_r2' % (d), loca=loca4)
                                        G.add_edge('%s_r1' % (c), '%s_r2' % (d), weight=self.get_time(loca3, loca4))

#============================================== remove edges weighted 0=================================================
                                        for n, nbrs in G.adjacency_iter():
                                            for nbr, eattr in nbrs.items():
                                                data = eattr['weight']
                                                if data == 0.0:
                                                    G.remove_edge('%s' % (n), '%s' % (nbr))

#============================================== final connect with 'end'node============================================

                                        G.add_edge('%s_r2' % (d), 'end' ,weight = self.get_time(loca4,end_loca))

        #print G.node
        #print G.edge


        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        nx.draw_networkx(G ,arrows=True,with_labels=True)
        plt.show()
        print 'SSR1R2', path['start']['end'] , length['start']['end']
        return path['start']['end'] , length['start']['end']


#=======================================================================================================================



    def dijk_ssr2r1(self, rs, output): # ex :output = ['10','18]
        G = nx.Graph()
        G.add_node('start',loca=[0,0,0])
        G.add_node('end',loca=[0,0,0])
        rack = self.adjust_rs(rs)
        output_list = output.replace(" ", "").split(",")
        outputs = [output_list[i:i+2] for i in range(0, len(output_list), 2)]
        outputs = outputs[0]
        init_loca = [0,0,0]
        end_loca = [0,0,0]
# ============================================== create first 'S'=======================================================
        for a, item in enumerate(rack):
            if item == '-1' :
                loca1 = self.loca_calculate(a)
                #print loca1
                G.add_node('%s_s1'%(a),loca=loca1)
                G.add_edge('start', '%s_s1'%(a), weight = self.get_time(init_loca,loca1))

#============================================== create second 'S'=======================================================

                for b, item in enumerate(rack):
                    if item == '-1' :
                        loca2 = self.loca_calculate(b)
                        G.add_node('%s_s2'%(b),loca=loca2)
                        G.add_edge('%s_s1'%(a), '%s_s2'%(b), weight = self.get_time(loca1,loca2))

#============================================== remove edges weighted 0=================================================
                        for n,nbrs in G.adjacency_iter():
                            for nbr,eattr in nbrs.items():
                                data = eattr['weight']
                                if data == 0.0:
                                    G.remove_edge('%s'%(n), '%s'%(nbr))

# ============================================== create 'R2R1'============================================================

                        for c, item in enumerate(rack):
                            loca3 = self.loca_calculate(c)
                            if item == outputs[1]:
                                G.add_node('%s_r2' % (c), loca=loca3)
                                G.add_edge('%s_s2' % (b), '%s_r2' % (c), weight=self.get_time(loca2, loca3))

                                for d, item in enumerate(rack):
                                    loca4 = self.loca_calculate(d)
                                    if item == outputs[0]:
                                        G.add_node('%s_r1' % (d), loca=loca4)
                                        G.add_edge('%s_r2' % (c), '%s_r1' % (d), weight=self.get_time(loca3, loca4))

#============================================== remove edges weighted 0=================================================
                                        for n, nbrs in G.adjacency_iter():
                                            for nbr, eattr in nbrs.items():
                                                data = eattr['weight']
                                                if data == 0.0:
                                                    G.remove_edge('%s' % (n), '%s' % (nbr))
#============================================== final connect with 'end'node============================================
                                        G.add_edge('%s_r1' % (d), 'end' ,weight = self.get_time(loca4,end_loca))

        #print G.node
        #print G.edge


        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        nx.draw_networkx(G ,arrows=True,with_labels=True)
        plt.show()
        print 'SSR2R1', path['start']['end'] , length['start']['end']
        return path['start']['end'] , length['start']['end']




test = action()
rs1 = test.rs1
output = test.output
#print test.rs1
#print output_list
print test.dijk_ssr1r2(rs1,output)
print test.dijk_ssr2r1(rs1,output)
