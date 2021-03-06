from problemIO import problemreader
import networkx as nx
import math
import solution
from collections import Counter
import matplotlib.pyplot as plt
import action
from simulator import nextstate

class ABC_Action(object):

    yspeed = 2.
    zspeed = 1.

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

    def abc_action_SSR1R2(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_c = {}
        # rs_a = []
        # rs_b = []
        # rs_c = []
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
            rs0.update({i:self.get_time([0,0,0],self.loca_calculate(i,column,floor))})
        for j in range(len(rs0)):
           if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
               rs_a.update({j:rs[j]})
           elif rs0.get(j) > (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(j) <= ((self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor))*2) / 3):
               rs_b.update({j:rs[j]})
           else:
               rs_c.update({j:rs[j]})

        # for j in range(len(rs0)):
        #     if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
        #         rs_a.append(j)
        #     elif rs0.get(j) > (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(j) <= ((self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor))*2) / 3):
        #         rs_b.append(j)
        #     else:
        #         rs_c.append(j)

        #print rs_a
        #print rs_b
        #print rs_c
        #print rs

        # start creating first S node
        if rs.count(input[0]) >= count_item.most_common(int(round(len(count_item)/3)))[-1][1]:
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

            elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        elif rs.count(input[0]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                        rs.count(input[0]) >= count_item.most_common(int(round(2* len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        else:
            if -1 in rs_c.values():
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))


        # finish creating first S nodes


        # start creating second S node
        if G.number_of_nodes() == 3 :
            for i, idx in enumerate(rs):
                if rs[i] == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    G.add_node('%s_s2' % loca1, loca = loca1, phase = 2)


        else :
            if rs.count(input[1]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

            elif rs.count(input[1]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                            rs.count(input[1]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
                if -1 in rs_b.values():
                    for i, idx in enumerate(rs_b):
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

                elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

            else:
                if -1 in rs_c.values():
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

                elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

                elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
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
        #
        # for n, nbrs in G.adjacency_iter():
        #     for nbr, eattr in nbrs.items():
        #         data = eattr['weight']
        #         if float(data) == 0:
        #             G.remove_edge('%s' % n, '%s' % nbr)


        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR1R2', path, length, self.print_dijk(G), io

    def abc_action_SSR2R1(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_c = {}
        # rs_a = []
        # rs_b = []
        # rs_c = []
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
            if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
                rs_a.update({j: rs[j]})
            elif rs0.get(j) > (
                self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(
                    j) <= (
                (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 2) / 3):
                rs_b.update({j: rs[j]})
            else:
                rs_c.update({j: rs[j]})

        # for j in range(len(rs0)):
        #     if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
        #         rs_a.append(j)
        #     elif rs0.get(j) > (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(j) <= ((self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor))*2) / 3):
        #         rs_b.append(j)
        #     else:
        #         rs_c.append(j)



        # start creating first S node
        if rs.count(input[0]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        elif rs.count(input[0]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                        rs.count(input[0]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        else:
            if -1 in rs_c.values():
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # start creating second S node

        if G.number_of_nodes() == 3 :
            for i, idx in enumerate(rs):
                if rs[i] == -1:
                    loca1 = self.loca_calculate(idx, column, floor)
                    G.add_node('%s_s2' % loca1, loca = loca1, phase = 2)

        else :
            if rs.count(input[1]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

            elif rs.count(input[1]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                            rs.count(input[1]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
                if -1 in rs_b.values():
                    for i, idx in enumerate(rs_b):
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

                elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

            else:
                if -1 in rs_c.values():
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

                elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=2)

                elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                    for i, idx in enumerate(rs_a):
                        if rs_a.get(idx) == -1:
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

    def abc_action_SR1SR2(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_c = {}
        # rs_a = []
        # rs_b = []
        # rs_c = []
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
            if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
                rs_a.update({j: rs[j]})
            elif rs0.get(j) > (
                        self.get_time([0, 0, 0],
                                      self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(
                j) <= (
                        (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 2) / 3):
                rs_b.update({j: rs[j]})
            else:
                rs_c.update({j: rs[j]})

        # for j in range(len(rs0)):
        #     if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
        #         rs_a.append(j)
        #     elif rs0.get(j) > (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(j) <= ((self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor))*2) / 3):
        #         rs_b.append(j)
        #     else:
        #         rs_c.append(j)



        # start creating first S node
        if rs.count(input[0]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        elif rs.count(input[0]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                        rs.count(input[0]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        else:
            if -1 in rs_c.values():
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # create first R node

        if output[0] in rs_a.values() and input[1] in rs_a.values():

            for b, item2 in enumerate(rs_a):
                loca2 = self.loca_calculate(item2, column, floor)
                if rs_a.get(item2) == output[0]:

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

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR1SR2', path, length, self.print_dijk(G), io

        elif output[0] in rs_b.values() and input[1] in rs_b.values():
            for b, item2 in enumerate(rs_b):
                loca2 = self.loca_calculate(item2, column, floor)
                if rs_b.get(item2) == output[0]:

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

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR1SR2', path, length, self.print_dijk(G), io

        elif output[0] in rs_c.values() and input[1] in rs_c.values():

            for b, item2 in enumerate(rs_c):
                loca2 = self.loca_calculate(item2, column, floor)
                if rs_c.get(item2) == output[0]:
                    G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                    # create s2
                    for c, item3 in enumerate(rs_c):
                        loca3 = self.loca_calculate(item3, column, floor)
                        if loca3[0] != loca2[0] and rs_c.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
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
            if rs.count(input[1]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            elif rs.count(input[1]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                            rs.count(input[1]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            else:
                if -1 in rs_c.values():
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
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


            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G ,arrows=True,with_labels=True)
            # plt.show()
            return 'SR1SR2', path, length, self.print_dijk(G), io

    def abc_action_SR2SR1(self, rs, column, floor, input, output):
        rs0 = {}
        rs_a = {}
        rs_b = {}
        rs_c = {}
        # rs_a = []
        # rs_b = []
        # rs_c = []
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
            if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
                rs_a.update({j: rs[j]})
            elif rs0.get(j) > (
                        self.get_time([0, 0, 0],
                                      self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(
                j) <= (
                        (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) * 2) / 3):
                rs_b.update({j: rs[j]})
            else:
                rs_c.update({j: rs[j]})

        # for j in range(len(rs0)):
        #     if rs0.get(j) <= (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3):
        #         rs_a.append(j)
        #     elif rs0.get(j) > (self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor)) / 3) and rs0.get(j) <= ((self.get_time([0, 0, 0], self.loca_calculate(column * floor * 2 - 1, column, floor))*2) / 3):
        #         rs_b.append(j)
        #     else:
        #         rs_c.append(j)



        # start creating first S node
        if rs.count(input[0]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        elif rs.count(input[0]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                        rs.count(input[0]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
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

            elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        else:
            if -1 in rs_c.values():
                for i, idx in enumerate(rs_c):
                    if rs_c.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                for i, idx in enumerate(rs_b):
                    if rs_b.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

            elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
                for i, idx in enumerate(rs_a):
                    if rs_a.get(idx) == -1:
                        loca1 = self.loca_calculate(idx, column, floor)
                        # print loca1
                        G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                        G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # finish creating first S nodes


        # create first R node

        if output[1] in rs_a.values() and input[1] in rs_a.values():

            for b, item2 in enumerate(rs_a):
                loca2 = self.loca_calculate(item2, column, floor)

                if rs_a.get(item2) == output[1]:
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

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            #nx.draw_networkx(G, arrows=True, with_labels=True)
            #plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR2SR1', path, length, self.print_dijk(G), io

        elif output[1] in rs_b.values() and input[1] in rs_b.values():

            for b, item2 in enumerate(rs_b):
                loca2 = self.loca_calculate(item2, column, floor)
                if rs_b.get(item2) == output[1]:
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

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            # nx.draw_networkx(G, arrows=True, with_labels=True)
            # plt.show()
            # print 'SR1SR2', path['start']['end'], length['start']['end']
            return 'SR2SR1', path, length, self.print_dijk(G), io

        elif output[1] in rs_c.values() and input[1] in rs_c.values():

            for b, item2 in enumerate(rs_c):
                loca2 = self.loca_calculate(item2, column, floor)
                if rs_c.get(item2) == output[1]:
                    G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                    # create s2
                    for c, item3 in enumerate(rs_c):
                        loca3 = self.loca_calculate(item3, column, floor)

                        if loca3[0] != loca2[0] and rs_c.get(item3) == -1 and loca3[1:3] == loca2[1:3]:
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
            if rs.count(input[1]) >= count_item.most_common(int(round(len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_a.values()) and (-1 not in rs_b.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            elif rs.count(input[1]) < count_item.most_common(int(round(len(count_item) / 3)))[-1][1] and \
                            rs.count(input[1]) >= count_item.most_common(int(round(2 * len(count_item) / 3)))[-1][1]:
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

                elif (-1 not in rs_b.values()) and (-1 not in rs_a.values()) and (-1 in rs.c.values()):
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

            else:
                if -1 in rs_c.values():
                    for i, idx in enumerate(rs_c):
                        if rs_c.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_c.values()) and (-1 in rs_b.values()):
                    for i, idx in enumerate(rs_b):
                        if rs_b.get(idx) == -1:
                            loca1 = self.loca_calculate(idx, column, floor)
                            # print loca1
                            G.add_node('%s_s2' % loca1, loca=loca1, phase=3)

                elif (-1 not in rs_c.values()) and (-1 not in rs_b.values()) and (-1 in rs.a.values()):
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

            path = nx.dijkstra_path(G, 'start', 'end')
            length = nx.dijkstra_path_length(G, 'start', 'end')
            io = ['S', 'R', 'S', 'R']
            #nx.draw_networkx(G ,arrows=True,with_labels=True)
            #plt.show()
            return 'SR2SR1', path, length, self.print_dijk(G), io


    def abc(self, rs, column, floor, input,
             output):  # concatenate 4 solutions // input/output example : [51,1] = 1 cycle outputs

        a1, b1, c1, d1, e1 = self.abc_action_SSR1R2(rs, column, floor, input, output)
        a2, b2, c2, d2, e2 = self.abc_action_SSR2R1(rs, column, floor, input, output)
        a3, b3, c3, d3, e3 = self.abc_action_SR1SR2(rs, column, floor, input, output)
        a4, b4, c4, d4, e4 = self.abc_action_SR2SR1(rs, column, floor, input, output)
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

    def abc_idx(self, rs, column, floor, input, output, idx):

        io = input + output

        if idx == 0:
            a1, b1, c1, d1, e1 = self.abc_action_SSR1R2(rs, column, floor, input, output)
            io = [io[0], io[1], io[2], io[3]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime

        elif idx == 1:
            a2, b2, c2, d2, e2 = self.abc_action_SSR2R1(rs, column, floor, input, output)
            io = [io[0], io[1], io[3], io[2]]
            sol = solution.solution(d2, io, e2)
            cycletime = c2
            return sol, cycletime

        elif idx == 2:
            a3, b3, c3, d3, e3 = self.abc_action_SR1SR2(rs, column, floor, input, output)
            io = [io[0], io[2], io[1], io[3]]
            sol = solution.solution(d3, io, e3)
            cycletime = c3
            return sol, cycletime

        elif idx == 3:
            a4, b4, c4, d4, e4 = self.abc_action_SR2SR1(rs, column, floor, input, output)
            io = [io[0], io[3], io[1], io[2]]
            sol = solution.solution(d4, io, e4)
            cycletime = c4
            return sol, cycletime




if __name__ == '__main__':
    test = problemreader.ProblemReader(25)
    rs = test.get_problem(1).rack.status
    column = test.get_problem(1).rack.column
    floor = test.get_problem(1).rack.floor
    input = test.get_problem(1).input
    output = test.get_problem(1).output


    ts = ABC_Action()
    ac = action.action()
    cycletime = 0
    sm = nextstate.simul()
    cum_cycletime = 0
    cum_cycletime1 = 0

    rs1 = test.get_problem(1).rack.status




    for i in range(50):
        inputs = input[(i + 1) * 2 - 2:(i + 1) * 2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]
        print rs
        print rs1
        print inputs
        print outputs
        a, b = ts.abc(rs, column, floor, inputs, outputs)
        c, d = ac.dijk_srsr_density(rs1,column,floor,inputs,outputs,0)
        cum_cycletime += b
        cum_cycletime1 += d
        print a.loc, c.loc
        print b, d
        print cum_cycletime, cum_cycletime1
        rs = sm.change_rs(rs, column, floor, a)
        rs1 = sm.change_rs(rs1,column,floor,c)


    # for i in range(len(input)/2):
    #     inputs = input[(i+1)*2-2:(i+1)*2]
    #     outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]
    #     a,b = ac.dijk(rs,column,floor,inputs,outputs)
    #     cycletime += b
    #     rs = sm.change_rs(rs,column,floor,a)
    #
    # print cycletime

