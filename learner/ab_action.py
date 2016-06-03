from problemIO import problemreader
import networkx as nx
import math
import solution
from collections import Counter
import matplotlib.pyplot as plt
import action
from simulator import nextstate

class AB_Action(object):

    yspeed = 2.
    zspeed = 1.

    def __init__(self, ini_rs):
        self.ini_rs = Counter(ini_rs)
        self.ini_rs.pop(-1)

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

    def get_time(self, start, end):

        return max(abs((start[1] - end[1]) / self.yspeed), abs((start[2] - end[2]) / self.zspeed))

    def adjust_list(self, lst):
        for i,j in enumerate(lst):
            for k in range(len(j)):
                lst[i][k] = int(lst[i][k])
        return lst

    def print_dijk(self,G): # G = nx.graph()
        path = nx.dijkstra_path(G,'start','end')
        sol_of_loca = path[1][:-3] + "/" + path[2][:-3] + "/" \
                      + path[3][:-3] + "/" + path[4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        return list_sol_of_loca

    def calculate_density_of_items(self,rs):
        return Counter(rs)

    def ab_action_SSR1R2(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_aa = []
        rs_bb = []

        count_item = Counter(rs)
        count_item.pop(-1)

        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]


        # print rs
        # print input
        # print output

        for i in range(len(rs)):
            rs0.update({i: self.get_time([0, 0, 0], self.loca_calculate(i, column, floor))})
        for j in range(len(rs0)):
            if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 0.8):
                rs_a.update({j: rs[j]})
            else:
                rs_b.update({j: rs[j]})
        for i in range(len(self.ini_rs)):
            if self.ini_rs.most_common(len(self.ini_rs)+1)[i][1] >= self.ini_rs.most_common(1)[0][1]*0.5:
                rs_aa.append(self.ini_rs.most_common(len(self.ini_rs)+1)[i][0])
            else : 
                rs_bb.append(self.ini_rs.most_common(len(self.ini_rs)+1)[i][0])
        
        
        # start creating first S node
        if input[0] in rs_aa:
            if -1 in rs_a.values():
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else :
                print "There is no space to save in rack"

        elif (input[0] not in rs_aa) and input[0] in rs_bb:
            if -1 in rs_b.values():
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        else:
            for i, idx in enumerate(rs):
                if idx == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    # print loca1
                    G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                    G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # start creating second S node
        if G.number_of_nodes() == 3:
            for i, idx in enumerate(rs):
                if rs[i] == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


        else:
            if input[1] in rs_aa:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                else:
                    print "There is no space to save in rack"

            elif (input[1] not in rs_bb) and input[1] in rs_bb:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

    
                else:
                    print "There is no space to save in rack"

            else:
                for i, idx in enumerate(rs):
                    if idx == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

        # finish creating second S nodes

        # start creating first, second R node
        for c, item3 in enumerate(rs):
            loca3 = self.loca_calculate(c, column, floor)
            if item3 == output[0]:
                G.add_node('%s_r1' % loca3, loca=loca3, phase=3)
                # G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rs):
            loca4 = self.loca_calculate(d, column, floor)
            if item4 == output[1]:
                G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

        # create edges
        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 2 and data4 == 3:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # remove edges weighted 0

        for n, nbrs in G.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                if float(data) == 0:
                    G.remove_edge('%s' % n, '%s' % nbr)

        path = nx.dijkstra_path(G, 'start', 'end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR1R2', path, length, self.print_dijk(G), io

    def ab_action_SSR2R1(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_aa = []
        rs_bb = []

        count_item = Counter(rs)
        count_item.pop(-1)

        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        # print rs
        # print input
        # print output

        for i in range(len(rs)):
            rs0.update({i: self.get_time([0, 0, 0], self.loca_calculate(i, column, floor))})
        for j in range(len(rs0)):
            if rs0.get(j) <= (
                self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 0.8):
                rs_a.update({j: rs[j]})
            else:
                rs_b.update({j: rs[j]})
        for i in range(len(self.ini_rs)):
            if self.ini_rs.most_common(len(self.ini_rs) + 1)[i][1] >= self.ini_rs.most_common(1)[0][1] * 0.5:
                rs_aa.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])
            else:
                rs_bb.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])

        # start creating first S node
        if input[0] in rs_aa:
            if -1 in rs_a.values():
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        elif (input[0] not in rs_aa) and input[0] in rs_bb:
            if -1 in rs_b.values():
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        else:
            for i, idx in enumerate(rs):
                if idx == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    # print loca1
                    G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                    G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # start creating second S node
        if G.number_of_nodes() == 3:
            for i, idx in enumerate(rs):
                if rs[i] == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


        else:
            if input[1] in rs_aa:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                else:
                    print "There is no space to save in rack"

            elif (input[1] not in rs_bb) and input[1] in rs_bb:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)


                else:
                    print "There is no space to save in rack"

            else:
                for i, idx in enumerate(rs):
                    if idx == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

        # finish creating second S nodes

        # start creating first, second R node
        for c, item3 in enumerate(rs):
            loca3 = self.loca_calculate(c, column, floor)
            if item3 == output[1]:
                G.add_node('%s_r2' % loca3, loca=loca3, phase=3)
                # G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rs):
            loca4 = self.loca_calculate(d, column, floor)
            if item4 == output[0]:
                G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

        # create edges
        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 2 and data4 == 3:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # remove edges weighted 0

        for n, nbrs in G.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                if float(data) == 0:
                    G.remove_edge('%s' % n, '%s' % nbr)

        path = nx.dijkstra_path(G, 'start', 'end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR2R1', path, length, self.print_dijk(G), io

    def ab_action_SR1SR2(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_aa = []
        rs_bb = []

        count_item = Counter(rs)
        count_item.pop(-1)

        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        # print rs
        # print input
        # print output

        for i in range(len(rs)):
            rs0.update({i: self.get_time([0, 0, 0], self.loca_calculate(i, column, floor))})
        for j in range(len(rs0)):
            if rs0.get(j) <= (
                self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 0.8):
                rs_a.update({j: rs[j]})
            else:
                rs_b.update({j: rs[j]})
        for i in range(len(self.ini_rs)):
            if self.ini_rs.most_common(len(self.ini_rs) + 1)[i][1] >= self.ini_rs.most_common(1)[0][1] * 0.5:
                rs_aa.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])
            else:
                rs_bb.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])

        # start creating first S node
        if input[0] in rs_aa:
            if -1 in rs_a.values():
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        elif (input[0] not in rs_aa) and input[0] in rs_bb:
            if -1 in rs_b.values():
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        else:
            for i, idx in enumerate(rs):
                if idx == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    # print loca1
                    G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                    G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # create first R node

        if output[0] in rs_aa and input[1] in rs_aa:
            if output[0] in rs_a.values():

                for b, item2 in enumerate(rs_a):
                    if rs_a.get(item2) == output[0]:
                        loca2 = self.loca_calculate(item2, column, floor)

                        G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_a):
                            loca3 = self.loca_calculate(item3, column, floor)
                            if loca3[0] != loca2[0] and rs_a.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            elif (output[0] not in rs_a.values()) and (output[0] in rs_b.values()):
                for c, item3 in enumerate(rs_b):
                    if rs_b.get(item3) == output[0]:
                        loca2 = self.loca_calculate(item3, column, floor)

                        G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_b):
                            loca3 = self.loca_calculate(item3, column, floor)

                            if loca3[0] != loca2[0] and rs_b.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            # create r2
            for d, item4 in enumerate(rs):
                if item4 == output[1]:
                    loca4 = self.loca_calculate(d, column, floor)
                    G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR1SR2', path, length, self.print_dijk(G), io

        elif output[0] in rs_bb and input[1] in rs_bb:
            if output[0] in rs_b.values():

                for b, item2 in enumerate(rs_b):
                    if rs_b.get(item2) == output[0]:
                        loca2 = self.loca_calculate(item2, column, floor)

                        G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_b):
                            loca3 = self.loca_calculate(item3, column, floor)
                            if loca3[0] != loca2[0] and rs_b.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            elif (output[0] not in rs_b.values()) and (output[0] in rs_a.values()):
                for c, item3 in enumerate(rs_a):
                    if rs_a.get(item3) == output[0]:
                        loca2 = self.loca_calculate(item3, column, floor)

                        G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_a):
                            loca3 = self.loca_calculate(item3, column, floor)

                            if loca3[0] != loca2[0] and rs_a.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))


            # create r2
            for d, item4 in enumerate(rs):
                if item4 == output[1]:
                    loca4 = self.loca_calculate(d, column, floor)
                    G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR1SR2', path, length, self.print_dijk(G), io


        # R1 and S2 are in different areas
        else:

            for d, item4 in enumerate(rs):
                loca4 = self.loca_calculate(d, column, floor)
                if item4 == output[0]:
                    G.add_node('%s_r1' % loca4, loca=loca4, phase=2)

                    # start creating second S node
            if input[1] in rs_aa:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            elif input[1] not in rs_aa and input[1] in rs_bb:
                if -1 in rs_b.values():
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)


            # finish creating second S nodes

            # start creating second R node


            for d, item4 in enumerate(rs):
                loca4 = self.loca_calculate(d, column, floor)
                if item4 == output[1]:
                    G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                    # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

            # create edges
            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 2 and data4 == 3:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            # remove edges weighted 0

            for n, nbrs in G.adjacency_iter():
                for nbr, eattr in nbrs.items():
                    data = eattr['weight']
                    if float(data) == 0:
                        G.remove_edge('%s' % n, '%s' % nbr)

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r1' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G ,arrows=True,with_labels=True)
            # plt.show()
            return 'SR1SR2', path, length, self.print_dijk(G), io

    def ab_action_SR2SR1(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_aa = []
        rs_bb = []

        count_item = Counter(rs)
        count_item.pop(-1)

        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        # print rs
        # print input
        # print output

        for i in range(len(rs)):
            rs0.update({i: self.get_time([0, 0, 0], self.loca_calculate(i, column, floor))})
        for j in range(len(rs0)):
            if rs0.get(j) <= (
                        self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 0.8):
                rs_a.update({j: rs[j]})
            else:
                rs_b.update({j: rs[j]})
        for i in range(len(self.ini_rs)):
            if self.ini_rs.most_common(len(self.ini_rs) + 1)[i][1] >= self.ini_rs.most_common(1)[0][1] * 0.5:
                rs_aa.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])
            else:
                rs_bb.append(self.ini_rs.most_common(len(self.ini_rs) + 1)[i][0])

        # start creating first S node
        if input[0] in rs_aa:
            if -1 in rs_a.values():
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        elif (input[0] not in rs_aa) and input[0] in rs_bb:
            if -1 in rs_b.values():
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            else:
                print "There is no space to save in rack"

        else:
            for i, idx in enumerate(rs):
                if idx == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    # print loca1
                    G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                    G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # create first R node

        if output[1] in rs_aa and input[1] in rs_aa:
            if output[1] in rs_a.values():
                for b, item2 in enumerate(rs_a):
                    if rs_a.get(item2) == output[1]:
                        loca2 = self.loca_calculate(item2, column, floor)

                        G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_a):
                            loca3 = self.loca_calculate(item3, column, floor)
                            if loca3[0] != loca2[0] and rs_a.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            elif (output[1] not in rs_a.values()) and (output[1] in rs_b.values()):
                for c, item3 in enumerate(rs_b):
                    if rs_b.get(item3) == output[1]:
                        loca2 = self.loca_calculate(item3, column, floor)

                        G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                        # create s2
                        for c, item3 in enumerate(rs_b):
                            loca3 = self.loca_calculate(item3, column, floor)

                            if loca3[0] != loca2[0] and rs_b.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            elif loca3 == loca2:
                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            # create r2
            for d, item4 in enumerate(rs):
                if item4 == output[0]:
                    loca4 = self.loca_calculate(d, column, floor)
                    G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR2SR1', path, length, self.print_dijk(G), io


        elif output[1] in rs_bb and input[1] in rs_bb:

            if output[1] in rs_b.values():

                for b, item2 in enumerate(rs_b):

                    if rs_b.get(item2) == output[1]:

                        loca2 = self.loca_calculate(item2, column, floor)

                        G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                        # create s2

                        for c, item3 in enumerate(rs_b):

                            loca3 = self.loca_calculate(item3, column, floor)

                            if loca3[0] != loca2[0] and rs_b.get(item3) == -1 and loca3[1:3] == loca2[1:3]:

                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)

                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                            elif loca3 == loca2:

                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)

                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))



            elif (output[1] not in rs_b.values()) and (output[1] in rs_a.values()):

                for c, item3 in enumerate(rs_a):

                    if rs_a.get(item3) == output[1]:

                        loca2 = self.loca_calculate(item3, column, floor)

                        G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                        # create s2

                        for c, item3 in enumerate(rs_a):

                            loca3 = self.loca_calculate(item3, column, floor)

                            if loca3[0] != loca2[0] and rs_a.get(item3) == -1 and loca3[1:3] == loca2[1:3]:

                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)

                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                            elif loca3 == loca2:

                                G.add_node('%s_s2' % loca3, loca=loca3, phase=3)

                                G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

            # create r2
            for d, item4 in enumerate(rs):
                if item4 == output[0]:
                    loca4 = self.loca_calculate(d, column, floor)
                    G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR2SR1', path, length, self.print_dijk(G), io


        # R1 and S2 are in different areas
        else:

            for d, item4 in enumerate(rs):
                loca4 = self.loca_calculate(d, column, floor)
                if item4 == output[1]:
                    G.add_node('%s_r2' % loca4, loca=loca4, phase=2)

                    # start creating second S node
            if input[1] in rs_aa:
                if -1 in rs_a.values():
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_a.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            elif input[1] not in rs_aa and input[1] in rs_bb:
                if -1 in rs_b.values():
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_b.values()) and (-1 in rs_a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            # finish creating second S nodes

            # start creating second R node


            for d, item4 in enumerate(rs):
                loca4 = self.loca_calculate(d, column, floor)
                if item4 == output[0]:
                    G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                    G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                    # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

            # create edges
            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 2:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 2 and data4 == 3:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 3 and data4 == 4:
                        G.add_edge(a, b, weight=self.get_time(data1, data3))

            # remove edges weighted 0

            for n, nbrs in G.adjacency_iter():
                for nbr, eattr in nbrs.items():
                    data = eattr['weight']
                    if float(data) == 0:
                        G.remove_edge('%s' % n, '%s' % nbr)

            for a, d in G.nodes_iter(data=True):
                data1 = d['loca']
                data2 = d['phase']
                for b, e in G.nodes_iter(data=True):
                    data3 = e['loca']
                    data4 = e['phase']
                    if data2 == 1 and data4 == 3 and data1 == data3:
                        if data1[0] == 0:
                            data1[0] = 1
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)
                        elif data1[0] == 1:
                            data1[0] = 0
                            if G.has_edge('%s_r2' % data1, '%s_s2' % data3) == True:
                                G.remove_edge('%s_r2' % data1, '%s_s2' % data3)

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G ,arrows=True,with_labels=True)
            # plt.show()
            return 'SR2SR1', path, length, self.print_dijk(G), io

    def ab_action(self, rs, column, floor, input,
            output):  # concatenate 4 solutions // input/output example : [51,1] = 1 cycle outputs

        a1, b1, c1, d1, e1 = self.ab_action_SSR1R2(rs, column, floor, input, output)
        a2, b2, c2, d2, e2 = self.ab_action_SSR2R1(rs, column, floor, input, output)
        a3, b3, c3, d3, e3 = self.ab_action_SR1SR2(rs, column, floor, input, output)
        a4, b4, c4, d4, e4 = self.ab_action_SR2SR1(rs, column, floor, input, output)
        io = input + output
    
        if min(c1, c2, c3, c4) == c1:
            io = [io[0], io[1], io[2], io[3]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime
        elif min(c1, c2, c3, c4) == c2:
            io = [io[0], io[1], io[3], io[2]]
            sol = solution.solution(d2, io, e2)
            cycletime = c2
            return sol, cycletime
        elif min(c1, c2, c3, c4) == c3:
            io = [io[0], io[2], io[1], io[3]]
            sol = solution.solution(d3, io, e3)
            cycletime = c3
            return sol, cycletime
        elif min(c1, c2, c3, c4) == c4:
            io = [io[0], io[3], io[1], io[2]]
            sol = solution.solution(d4, io, e4)
            cycletime = c4
            return sol, cycletime


    def ab_idx(self, rs, column, floor, input, output, idx):
        io = input + output
    
        if idx == 0:
            a1, b1, c1, d1, e1 = self.ab_action_SSR1R2(rs, column, floor, input, output)
            io = [io[0], io[1], io[2], io[3]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime
    
        elif idx == 1:
            a2, b2, c2, d2, e2 = self.ab_action_SSR2R1(rs, column, floor, input, output)
            io = [io[0], io[1], io[3], io[2]]
            sol = solution.solution(d2, io, e2)
            cycletime = c2
            return sol, cycletime

        elif idx == 2:
            a3, b3, c3, d3, e3 = self.ab_action_SR1SR2(rs, column, floor, input, output)
            io = [io[0], io[2], io[1], io[3]]
            sol = solution.solution(d3, io, e3)
            cycletime = c3
            return sol, cycletime

        elif idx == 3:
            a4, b4, c4, d4, e4 = self.ab_action_SR2SR1(rs, column, floor, input, output)
            io = [io[0], io[3], io[1], io[2]]
            sol = solution.solution(d4, io, e4)
            cycletime = c4
            return sol, cycletime


if __name__ == '__main__':
    test = problemreader.ProblemReader(26)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor
    input = test.get_problem(1).input
    output = test.get_problem(1).output


    ts = AB_Action(rs)
    ac = action.action()
    cycletime = 0
    sm = nextstate.simul()
    cum_cycletime = 0
    cum_cycletime1 = 0
    input_count = 0
    output_count = 0
    diff_between_cycletime = 0

    rs1 = test.get_problem(1).rack.status


    index = []
    diff = []



    for i in range(len(input)/2):
        inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]


        print i
        print rs

        # print rs1
        print inputs, outputs
        # print outputs
        # print input_count
        # print output_count

        a, b = ts.ab_action(rs,column,floor,inputs,outputs)
        c, d = ac.dijk_srsr_density(rs1,column,floor,inputs,outputs,0)
        cum_cycletime += b
        cum_cycletime1 += d
        # print c.loc, c.oper, c.type
        print b, d
        print cum_cycletime, cum_cycletime1
        diff_between_cycletime = cum_cycletime - cum_cycletime1
        rs = sm.change_rs(rs, column, floor, a)
        rs1 = sm.change_rs(rs1,column,floor,c)

        index.append(i)
        diff.append(diff_between_cycletime)
        plt.plot(index,diff,'ro-')
    plt.show()

    # rs = [5, 5, 2, -1, 5, 16, 0, 20, 8, 19, 2, 21, 15, 1, 1, 13, 25, 6, 7, 18, 12, 15, 0, 0, 17, 14, -1, 7, 9, -1, 4, 1, 5, 21, 25, 2, 3, -1, 6, 5, 14, -1, 13, 1, 1, 14, -1, -1, 16, -1, 0, -1, -1, 0, 10, 4, 14, 6, 21, 1, 5, 9, 5, 12, 13, 5, -1, 8, 1, 3, -1, 2, -1, 10, 11, 5, 1, 6, 12, 19, 14, 22, 9, 25, -1, 25, 9, -1, 2, 8, -1, 10, -1, 0, -1, 5, 3, 3, 11, 1, 13, 4, 11, 14, 2, 5, 14, 1, 19, 5, 0, 5, 15, 0, 1, 7, 22, 24, 13, 20, 6, 8, 2, 13, 6, 5, 17, -1, -1, 19, 0, 2, -1, 17, -1, 6, 19, 14, 12, 4, 17, 20, 9, 13, 5, 17, 16, 14, 8, -1, 21, 20, -1, 13, 3, 7, 12, 21, 3, 24, 20, -1, 2, 4, 10, -1, 16, 12, 10, 23, 18, -1, 18, 18, -1, -1, 4, 11, 14, 0, -1, -1, 25, 0, 16, 9, 1, 20, 9, -1, 16, 8, -1, 18, -1, 24, 11, 7, 18, 15, 0, -1, 1, 0, 17, -1, 20, 2, -1, 14, 4, 2, 7, -1, 1, 10, 7, 20, 3, -1, -1, 11, 19, 8, 17, -1, 0, 7, 6, -1, 19, -1, 16, 3, 9, 3, 20, 17, 17, -1, 13, -1, 21, -1, 2, 9, 3, -1, 22, 21, 8, 7, 17, 22, 16, 18, 5, 9, -1, 16, 8, -1, 17, 14, 15, -1, 0, -1, 6, 0, -1, 10, 16, 8, 7, 5, 10, 7, 4, 1, -1, 16, -1, 24, 25, -1, 5, 11, 9, -1, 1, 1, 8, -1, -1, -1, 4, 1, 0, 8, 10, 23, -1, -1, 10, 0, -1, 18, 21, 6, 14, 0, 3, 11, 17, 10, 21, 6, 22, -1, 9, 11, 2, -1, 17, -1, 9, -1, 16, 13, -1, 25, 8, 12, 14, 15, 14, 17, -1, 14, 4, 10, 13, 21, 11, 21, -1, -1, 13, -1, 1, 8, 10, 2, 4, 23, 17, 13, 13, -1, 11, 0, 14, 7, 1, -1, 20, 18, 4, 4, 7, 21, 12, 2, 23, 23, 9, 4, 1, 9, 18, -1, 6, 11, -1, 2, 11, 15, -1, -1, 14, 5, 16, 17, 1, 11, 2, 24, -1, -1, 18, 23, 5, 12, 17, 7, 25, -1, 24, 9, -1, 1, -1, 17, 20, 7, 20, 9, -1, 14, 13, 15, 1, -1, 1, 12, 1, 17, 1, 20, 22, -1, -1, 7, 14, 17, 12, 13, 16, -1, 16, 2, 4, 5, 6, 19, 22, 1, 17, 14, 23, -1, -1, 9, 17, -1, 19, 20, -1, 13, 2, 9, 1, 14, 21, 4, 18, 16, 3, 14, 13, -1, 20, 9, 2, 10, 6, 6, 0, 4, 5, 5, 13, 9, 25, 9, 2, -1, -1, -1, 22, 2, -1, -1, 6, 3, 3, 15, -1, -1, 5, 16, 19, 10, -1, -1, -1, 16, 3, 6, 25, -1, 11, 16, 13, -1, 15, 3, 8, 11, 13, 18, 6, 18, 2, 3, -1, 24, -1, 14, 11, 5, 12, -1, 7, 11, 25, 19, 6, 0, 18, 8, 8, 4, 6, 14, 12, 7, -1, 4, 7, -1, 15, 12, -1, 6, 8, 17, 5, -1, 22, 25, 17, 4, 13, -1, 17, -1, 9, 0, 10, -1, 25, 10, 13, 13, 1, 21, -1, -1, 23, 21, 7, 4, 7, 14, 16, 2, -1, 19, 2, 1, 5, -1, 18, 10, 1, 9, 20, 17, 5, 14, -1, 15, 1, 16, 5, 11, 13, 1, 3, 5, 2, -1, -1, 9, 24, 12, 14, 7, 1, 2, 19, 1, 10, 3, 0, -1, 19, 11, 24, -1, 9, 9, 12, 5, 3, 12, 1, 2, 9, 18, 23, 17, 9, 12, -1, 25, 4, 8, -1, 9, 8, -1, 10, 8, 24, 5, -1, 15, 17, 1, -1, 6, 5, -1, 11, 23, -1, -1, 18, -1, 23, 2, 18, -1, 2, 16, -1, -1, 6, 23, 5, 4, 13, 3, 17, -1, 8, 19, 5, -1, 22, 1, 20, 14, 0, 6, -1, 14, 0, 13, -1, 17, -1, 16, 14, 17, -1, 4, -1, -1, -1, -1, 11, -1, 8, 12, 20, 13, 10, 7, 18, 18, 14, 10, -1, -1, -1, 16, 13, 14, 22, -1, 5, 18, 7, 19, 16, 4, -1, 16, 4, 7, -1, 4, 2, 8, 10, 9, 0, 8, 3, 7, -1, -1, 24, 18, 9, 9, 11, 18, 4, -1, 15, 10, -1, 20, 9, 18, 4, -1, -1, 12, 18, -1, 15, 4, 14, 18, -1, 14, -1, 14, -1, -1, 24, -1, 4, 0, 6, 20, 1, 8, 6, 18, 1, 2, -1, 21]
    #
    # input = [1, 10]
    # output = [17, 17]
    # a, b = ts.ab_idx(rs, column, floor, input, output, 3)
    # # c,d = ac.dijk_srsr_density(rs,column,floor,input,output,0)

