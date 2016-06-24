from problemIO import problemreader
import networkx as nx
import math
import solution
from simulator import nextstate
from simulator import visualize_rack
from collections import Counter
import matplotlib.pyplot as plt


class action(object):

    yspeed = 3.
    zspeed = 1.

    def loca_calculate(self,index,size_h,size_v):

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

    def adjust_rs(self, rs1):
        rs1 = rs1.replace(" ", "")
        rs1 = rs1.split(",")

        return rs1

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


    def find_another_dijk_solution(self,G,source,target,cutoff):
        G0 = G
        G1 = G
        G2 = G
        G3 = G
        G4 = G

        path = nx.dijkstra_path(G,source,target)

        G0[path[0]][path[1]]['weight'] += 0.0001
        G1[path[1]][path[2]]['weight'] += 0.0001
        G2[path[2]][path[3]]['weight'] += 0.0001
        G3[path[3]][path[4]]['weight'] += 0.0001
        G4[path[4]][path[5]]['weight'] += 0.0001

        path_0 = nx.dijkstra_path(G0,source,target)
        length_0 = nx.dijkstra_path_length(G0,source,target)
        path_1 = nx.dijkstra_path(G1,source,target)
        length_1 = nx.dijkstra_path_length(G1,source,target)
        path_2 = nx.dijkstra_path(G2,source,target)
        length_2 = nx.dijkstra_path_length(G2,source,target)
        path_3 = nx.dijkstra_path(G3,source,target)
        length_3 = nx.dijkstra_path_length(G3,source,target)
        path_4 = nx.dijkstra_path(G4,source,target)
        length_4 = nx.dijkstra_path_length(G4,source,target)

        # all_path = [path1, path2, path3, path4, path5]
        # all_length = [length1, length2, length3, length4, length5]
        selected_path_0 = []
        selected_length_0 = []
        selected_path_1 = []
        selected_length_1 = []
        selected_path_2 = []
        selected_length_2 = []
        selected_path_3 = []
        selected_length_3 = []
        selected_path_4 = []
        selected_length_4 = []
        trash_path_0 = []
        trash_path_1 = []
        trash_path_2 = []
        trash_path_3 = []
        trash_path_4 = []

        if path_0 != path and length_0 == cutoff:
            selected_path_0.append(path_0)
            selected_length_0.append(length_0)
            while bool(trash_path_0) == False :
                G0[path_0[0]][path_0[1]]['weight'] += 0.0001
                path_0 = nx.dijkstra_path(G0, source, target)
                length_0 = nx.dijkstra_path_length(G0, source, target)
                if path_0 in selected_path_0:
                    trash_path_0.append(path_0)
                elif length_0 == cutoff:
                    selected_path_0.append(path_0)
                    selected_length_0.append(length_0)


        if path_1 != path and length_1 == cutoff:
            selected_path_1.append(path_1)
            selected_length_1.append(length_1)
            while bool(trash_path_1) == False :
                G1[path_1[1]][path_1[2]]['weight'] += 0.0001
                path_1 = nx.dijkstra_path(G1, source, target)
                length_1 = nx.dijkstra_path_length(G1, source, target)
                if path_1 in selected_path_1:
                    trash_path_1.append(path_1)
                elif length_1 == cutoff:
                    selected_path_1.append(path_1)
                    selected_length_1.append(length_1)

        if path_2 != path and length_2 == cutoff:
            selected_path_2.append(path_2)
            selected_length_2.append(length_2)
            while bool(trash_path_2) == False :
                G2[path_2[2]][path_2[3]]['weight'] += 0.0001
                path_2 = nx.dijkstra_path(G2, source, target)
                length_2 = nx.dijkstra_path_length(G2, source, target)
                if path_2 in selected_path_2:
                    trash_path_2.append(path_2)
                elif length_2 == cutoff:
                    selected_path_2.append(path_2)
                    selected_length_2.append(length_2)

        if path_3 != path and length_3 == cutoff:
            selected_path_3.append(path_3)
            selected_length_3.append(length_3)
            while bool(trash_path_3) == False :
                G3[path_3[3]][path_3[4]]['weight'] += 0.0001
                path_3 = nx.dijkstra_path(G3, source, target)
                length_3 = nx.dijkstra_path_length(G3, source, target)
                if path_3 in selected_path_3:
                    trash_path_3.append(path_3)
                elif length_3 == cutoff:
                    selected_path_3.append(path_3)
                    selected_length_3.append(length_3)

        if path_4 != path and length_4 == cutoff:
            selected_path_4.append(path_4)
            selected_length_4.append(length_4)
            while bool(trash_path_4) == False :
                G4[path_4[4]][path_4[5]]['weight'] += 0.0001
                path_4 = nx.dijkstra_path(G4, source, target)
                length_4 = nx.dijkstra_path_length(G4, source, target)
                if path_4 in selected_path_4:
                    trash_path_4.append(path_4)
                elif length_4 == cutoff:
                    selected_path_4.append(path_4)
                    selected_length_4.append(length_4)

        selected_path = selected_path_0 + selected_path_1 + selected_path_2 + selected_path_3 + selected_path_4
        selected_length = selected_length_0 + selected_length_1 + selected_length_2 + selected_length_3 + selected_length_4

        remove_dup_path = []
        remove_dup_length = []
        [remove_dup_path.append(x) for x in selected_path if x not in remove_dup_path]
        [remove_dup_length.append(x) for x in selected_length if x not in remove_dup_length]

        if bool(remove_dup_path) == True:
            # get maximun cycletime on 2Ss in solutions
            modify_list = []
            avg_cycletime_2Ss = []

            for i in range(len(remove_dup_path)):
                path = remove_dup_path[i]
                sol_of_loca = path[1][:-3] + "/" + path[2][:-3] + "/" \
                              + path[3][:-3] + "/" + path[4][:-3]
                sol_of_loca = sol_of_loca.replace("[", "")
                sol_of_loca = sol_of_loca.replace("]", "")
                sol_of_loca = sol_of_loca.replace(" ", "")
                list_sol_of_loca = sol_of_loca.split("/")
                list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
                list_sol_of_loca = self.adjust_list(list_sol_of_loca)
                modify_list.append(list_sol_of_loca)

            for j in range(len(modify_list)):
                avg_cycletime_2Ss.append(((self.get_time([0,0,0],modify_list[j][0]) + self.get_time([0,0,0],modify_list[j][2])) / 2))

            for i,j in enumerate(avg_cycletime_2Ss):
                if j is max(avg_cycletime_2Ss):
                    return modify_list[i]
        else:

            return remove_dup_path#, remove_dup_length



    def dijk_ssr1r2(self, rs, column, floor, outputs):# ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca,loca1))

                # create second 'S'
        for b, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(b, size_h, size_v)
                G.add_node('%s_s2' % loca2, loca=loca2, phase=2)
                #G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1, loca2))

        # create 'R1R2'
        for c, item3 in enumerate(rack):
            loca3 = self.loca_calculate(c, size_h, size_v)
            if item3 == outputs[0]:
                G.add_node('%s_r1' % loca3, loca=loca3, phase=3)
                #G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rack):
            loca4 = self.loca_calculate(d, size_h, size_v)
            if item4 == outputs[1]:
                G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                #G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 2 and data4 == 3:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4:
                    G.add_edge(a,b, weight=self.get_time(data1,data3))

        # remove edges weighted 0

        for n, nbrs in G.adjacency_iter():
            for nbr, eattr in nbrs.items():
                data = eattr['weight']
                # if float(data) == 0  and n != 'start' and n != 'end' and nbr != 'start' and nbr != 'end':
                if n[0:-3] == nbr[0:-3]:
                    G.remove_edge('%s' % n, '%s' % nbr)

        #print G.node
        #print G.edge

        #print 'end'

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR1R2', path, length, self.print_dijk(G), io

    def dijk_ssr2r1(self, rs, column, floor, outputs):  # ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

                # create second 'S'
        for b, item2 in enumerate(rack):
            if item2 == -1:
                loca2 = self.loca_calculate(b, size_h, size_v)
                G.add_node('%s_s2' % loca2, loca=loca2, phase=2)
                # G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1, loca2))

        # create 'R2R1'
        for c, item3 in enumerate(rack):
            loca3 = self.loca_calculate(c, size_h, size_v)
            if item3 == outputs[1]:
                G.add_node('%s_r2' % loca3, loca=loca3, phase=3)
                # G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

        for d, item4 in enumerate(rack):
            loca4 = self.loca_calculate(d, size_h, size_v)
            if item4 == outputs[0]:
                G.add_node('%s_r1' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))
                # G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

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
                # if float(data) == 0 and n != 'start' and n != 'end' and nbr != 'start' and nbr != 'end':
                if n[0:-3] == nbr[0:-3]:
                    G.remove_edge('%s' % n, '%s' % nbr)

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io= ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR2R1', path, length, self.print_dijk(G), io

    def dijk_sr1sr2(self, rs, column, floor, outputs): # ex :outputs = ['10','18']
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # create r1
        for b, item2 in enumerate(rack):
            loca2 = self.loca_calculate(b,size_h, size_v)
            if item2 == outputs[0]:
                G.add_node('%s_r1' % loca2, loca=loca2, phase=2)

                # create s2
                for c, item3 in enumerate(rack):
                    loca3 = self.loca_calculate(c, size_h, size_v)
                    # if loca3[0] != loca2[0] and item3 == -1 and loca3[1:3] == loca2[1:3] :
                    #     G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                    #     G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                    if loca3 == loca2:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

        """# create s2
        loca3 = self.loca_calculate(b,size_h, size_v)
        for c, item3 in enumerate(rack):
            # check the opposite side is empty
            loca5 = self.loca_calculate(c,size_h, size_v)
            if c != b and loca5[0] == -1 and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                loca3 = loca5
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
            else:
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))"""

        # create r2
        for d, item4 in enumerate(rack):
            if item4 == outputs[1]:
                loca4 = self.loca_calculate(d, size_h, size_v)
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
                if data2 == 3 and data4 == 4 and data1 != data3:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # for a, d in G.nodes_iter(data=True):
        #     data1 = d['loca']
        #     data2 = d['phase']
        #     for b, e in G.nodes_iter(data=True):
        #         data3 = e['loca']
        #         data4 = e['phase']
        #         # print data1, data2, data3, data4
        #         if data2 == 1 and data4 == 3 and data1 == data3 :
        #             print 'ok'
        #             if data1[0] == 0:
        #                 print 'ok2'
        #                 data1[0] = 1
        #                 if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True :
        #                     print 'ok3'
        #                     G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
        #             elif data1[0] == 1:
        #                 print 'ok4'
        #                 data1[0] = 0
        #                 if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True :
        #                     print 'ok5'
        #                     G.remove_edge('%s_r1' % data1, '%s_s2' % data3)







        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        # all_path = nx.all_shortest_paths(G,'start','end', 'weight')
        # path_1 = self.find_another_dijk_solution(G,'start','end',length)
        # path_0 = self.print_dijk(G)
        # if bool(path_1) == True:
        #     print str(path_0[0]) + " > " + str(path_1[0])
        #     print str(path_0[1]) + " > " + str(path_1[1])
        #     print str(path_0[2]) + " > " + str(path_1[2])
        #     print str(path_0[3]) + " > " + str(path_1[3])
        io = ['S', 'R', 'S', 'R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR1SR2', path['start']['end'], length['start']['end']
        # if bool(path_1) == True:
        #     return 'SR1SR2', path, length, path_1, io
        # else:
        #     return 'SR1SR2', path, length, self.print_dijk(G),io
        return 'SR1SR2', path, length, self.print_dijk(G), io

        # return [p for p in all_path]


    def dijk_sr2sr1(self, rs, column, floor, outputs):# ex :outputs = [10,18]
        G = nx.DiGraph()
        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # create r2
        for b, item2 in enumerate(rack):
            loca2 = self.loca_calculate(b, size_h, size_v)
            if item2 == outputs[1]:
                G.add_node('%s_r2' % loca2, loca=loca2, phase=2)

                # create s2
                for c, item3 in enumerate(rack):
                    loca3 = self.loca_calculate(c, size_h, size_v)
                    # if loca3[0] != loca2[0] and item3 == -1 and loca3[1:3] == loca2[1:3]:
                    #     G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                    #     G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                    if loca3 == loca2:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

        """# create s2
        loca3 = self.loca_calculate(b,size_h, size_v)
        for c, item3 in enumerate(rack):
            # check the opposite side is empty
            loca5 = self.loca_calculate(c,size_h, size_v)
            if c != b and loca5[0] == -1 and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                loca3 = loca5
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
            else:
                G.add_node('%s_s2' % loca3, loca=loca3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))"""

        # create r1
        for d, item4 in enumerate(rack):
            if item4 == outputs[0]:
                loca4 = self.loca_calculate(d, size_h, size_v)
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
                if data2 == 3 and data4 == 4 and data1 != data3 :
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # for a, d in G.nodes_iter(data=True):
        #     data1 = d['loca']
        #     data2 = d['phase']
        #     for b, e in G.nodes_iter(data=True):
        #         data3 = e['loca']
        #         data4 = e['phase']
        #         if data2 == 1 and data4 == 3 and data1 == data3:
        #             if data1[0] == 0:
        #                 data3[0] = 1
        #                 if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
        #                     G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
        #             elif data1[0] == 1:
        #                 data3[0] = 0
        #                 if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True:
        #                     G.remove_edge('%s_r1' % data1, '%s_s2' % data3)

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        # path_1 = self.find_another_dijk_solution(G,'start','end',length)
        # path_0 = self.print_dijk(G)
        # if bool(path_1) == True:
        #     print str(path_0[0]) + " > " + str(path_1[0])
        #     print str(path_0[1]) + " > " + str(path_1[1])
        #     print str(path_0[2]) + " > " + str(path_1[2])
        #     print str(path_0[3]) + " > " + str(path_1[3])
        io = ['S','R','S','R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR2SR1', path['start']['end'], length['start']['end']
        return 'SR2SR1', path, length, self.print_dijk(G), io

        # if bool(path_1) == True:
        #     return 'SR2SR1', path, length, path_1, io
        # else:
        #     return 'SR2SR1', path, length, self.print_dijk(G),io


    def dijk(self,rs,column,floor,input,output): # concatenate 4 solutions // input/output example : [51,1] = 1 cycle outputs

        a1,b1,c1,d1,e1 = self.dijk_ssr1r2(rs,column,floor,output)
        a2,b2,c2,d2,e2 = self.dijk_ssr2r1(rs,column,floor,output)
        a3,b3,c3,d3,e3 = self.dijk_sr1sr2(rs,column,floor,output)
        a4,b4,c4,d4,e4 = self.dijk_sr2sr1(rs,column,floor,output)
        io = input + output

        if min(c1,c2,c3,c4) == c1:
            io = [io[0],io[1],io[2],io[3]]
            sol = solution.solution(d1,io,e1)
            cycletime = c1
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c2:
            io = [io[0],io[1],io[3],io[2]]
            sol = solution.solution(d2,io,e2)
            cycletime = c2
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c3:
            io = [io[0],io[2],io[1],io[3]]
            sol = solution.solution(d3,io,e3)
            cycletime = c3
            return sol, cycletime
        elif min(c1,c2,c3,c4) == c4:
            io = [io[0],io[3],io[1],io[2]]
            sol = solution.solution(d4,io,e4)
            cycletime = c4
            return sol, cycletime


        #print action.dijk_ssr1r2(rs,size_h, size_v, output)
        #print action.dijk_ssr2r1(rs,size_h, size_v, output)
        #print action.dijk_sr1sr2(rs,size_h, size_v, output)
        #print action.dijk_sr2sr1(rs,size_h, size_v, output)

    def dijk_idx(self, rs, column, floor, input, output, idx):

        io = input + output

        if idx == 0:
            a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs,column,floor,output)
            io = [io[0],io[1],io[2],io[3]]
            sol = solution.solution(d1,io,e1)
            cycletime = c1
            return sol, cycletime

        elif idx == 1:
            a2, b2, c2, d2, e2 = self.dijk_ssr2r1(rs,column,floor,output)
            io = [io[0],io[1],io[3],io[2]]
            sol = solution.solution(d2,io,e2)
            cycletime = c2
            return sol, cycletime

        elif idx == 2:
            a3, b3, c3, d3, e3 = self.dijk_sr1sr2(rs,column,floor,output)
            io = [io[0],io[2],io[1],io[3]]
            sol = solution.solution(d3,io,e3)
            cycletime = c3
            return sol, cycletime

        elif idx == 3:
            a4, b4, c4, d4, e4 = self.dijk_sr2sr1(rs,column,floor,output)
            io = [io[0],io[3],io[1],io[2]]
            sol = solution.solution(d4,io,e4)
            cycletime = c4
            return sol, cycletime


    def dijk_all(self, rs, column, floor, input, output):
            return self.dijk_idx(rs,column,floor,input,output,0), self.dijk_idx(rs,column,floor,input,output,1), \
                   self.dijk_idx(rs,column,floor,input,output,2), self.dijk_idx(rs,column,floor,input,output,3),


    def dijk_2(self, rs, column, floor, input,
             output):  # concatenate 4 solutions // input/output example : [51,1] = 1 cycle outputs

        a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
        a2, b2, c2, d2, e2 = self.dijk_ssr2r1(rs, column, floor, output)
        a3, b3, c3, d3, e3 = self.dijk_sr1sr2(rs, column, floor, output)
        a4, b4, c4, d4, e4 = self.dijk_sr2sr1(rs, column, floor, output)
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


    def dijk_2_idx(self, rs, column, floor, input, output, idx):

        io = input + output

        if idx == 0:
            a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
            a2, b2, c2, d2, e2 = self.dijk_ssr2r1(rs, column, floor, output)
            if c1 <= c2:
                io = [io[0], io[1], io[2], io[3]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
            else:
                io = [io[0], io[1], io[3], io[2]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
        elif idx == 1:
            a3, b3, c3, d3, e3 = self.dijk_sr1sr2(rs, column, floor, output)
            a4, b4, c4, d4, e4 = self.dijk_sr2sr1(rs, column, floor, output)
            if c3 <= c4:
                io = [io[0], io[2], io[1], io[3]]
                sol = solution.solution(d3, io, e3)
                cycletime = c3
            else:
                io = [io[0], io[3], io[1], io[2]]
                sol = solution.solution(d4, io, e4)
                cycletime = c4
        return sol, cycletime

    def dijk_density(self,rs,column,floor,input,output,idx):
        if idx == 0:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 1:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 2:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 3:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 4:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 5:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 6:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 7:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = input + output
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime


    def dijk_srsr_density(self, rs, column, floor, input, output, idx):
        if idx == 0:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

        elif idx == 1:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 2:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
        elif idx == 3:
            if rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[1], input[0]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[0]) >= rs.count(output[1]):
                input = [input[0], input[1]]
                output = [output[1], output[0]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[0]) >= rs.count(input[1]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[1], input[0]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

            elif rs.count(input[1]) > rs.count(input[0]) and rs.count(output[1]) > rs.count(output[0]):
                input = [input[0], input[1]]
                output = [output[0], output[1]]
                io = [input[0], output[0], input[1], output[1]]
                a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

    def dijk_srsr_density_test_fixed_output(self, rs, column, floor, input, output):

        if output[0] <= output[1]:
            io = [input[0], output[0], input[1], output[1]]
            a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime

        elif output[1] < output[0]:
            io = [input[0], output[1], input[1], output[0]]
            a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime

    def dijk_srsr_faster_one(self, rs, column, floor, input, output):

        a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
        a2, b2, c2, d2, e2 = self.dijk_sr2sr1(rs, column, floor, output)

        if c1 <= c2:
            print "used sr1sr2"
            io = [input[0], output[0], input[1], output[1]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime
        elif c2 < c1:
            print 'used sr2sr1'
            io = [input[0], output[0], input[1], output[1]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime





    def dijk_srsr_with_abc_a(self, rs, column, floor, input, output): # large - few

        a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
        a2, b2, c2, d2, e2 = self.dijk_sr2sr1(rs, column, floor, output)

        if c1 <= c2 :
            if self.get_time([0, 0, 0], d1[0]) <= self.get_time([0, 0, 0], d1[2]) and input[0] <= input[1]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d1,io,e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) <= self.get_time([0, 0, 0], d1[2]) and input[1] < input[0]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) > self.get_time([0, 0, 0], d1[2]) and input[0] <= input[1]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) > self.get_time([0, 0, 0], d1[2]) and input[1] < input[0]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

        elif c1 > c2:
            if self.get_time([0, 0, 0], d2[0]) <= self.get_time([0, 0, 0], d2[2]) and input[0] <= input[1]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d2,io,e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) <= self.get_time([0, 0, 0], d2[2]) and input[1] < input[0]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) > self.get_time([0, 0, 0], d2[2]) and input[0] <= input[1]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) > self.get_time([0, 0, 0], d2[2]) and input[1] < input[0]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime

    def dijk_srsr_with_abc_b(self, rs, column, floor, input, output):  # few - large

        a1, b1, c1, d1, e1 = self.dijk_sr1sr2(rs, column, floor, output)
        a2, b2, c2, d2, e2 = self.dijk_sr2sr1(rs, column, floor, output)

        if c1 <= c2:
            if self.get_time([0, 0, 0], d1[0]) <= self.get_time([0, 0, 0], d1[2]) and input[0] <= input[1]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) <= self.get_time([0, 0, 0], d1[2]) and input[1] < input[0]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) > self.get_time([0, 0, 0], d1[2]) and input[0] <= input[1]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime
            elif self.get_time([0, 0, 0], d1[0]) > self.get_time([0, 0, 0], d1[2]) and input[1] < input[0]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d1, io, e1)
                cycletime = c1
                return sol, cycletime

        elif c1 > c2:
            if self.get_time([0, 0, 0], d2[0]) <= self.get_time([0, 0, 0], d2[2]) and input[0] <= input[1]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) <= self.get_time([0, 0, 0], d2[2]) and input[1] < input[0]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) > self.get_time([0, 0, 0], d2[2]) and input[0] <= input[1]:
                io = [input[0], output[0], input[1], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime
            elif self.get_time([0, 0, 0], d2[0]) > self.get_time([0, 0, 0], d2[2]) and input[1] < input[0]:
                io = [input[1], output[0], input[0], output[1]]
                sol = solution.solution(d2, io, e2)
                cycletime = c2
                return sol, cycletime


    def dijk_srsr_with_abc_idx(self, rs, column, floor, input, output, idx):
        if idx == 0:
            if output[0] < output[1]:
                output.reverse()
            return self.dijk_srsr_with_abc_a(rs, column, floor, input, output)
        elif idx == 1:
            if output[0] > output[1]:
                output.reverse()
            return self.dijk_srsr_with_abc_a(rs, column, floor, input, output)
        elif idx == 2:
            if output[0] < output[1]:
                output.reverse()
            return self.dijk_srsr_with_abc_b(rs, column, floor, input, output)
        elif idx == 3:
            if output[0] > output[1]:
                output.reverse()
            return self.dijk_srsr_with_abc_b(rs, column, floor, input, output)



if __name__ == '__main__':
    test = problemreader.ProblemReader(28)
    rs = test.get_problem(3).rack.status
    column = test.get_problem(3).rack.column
    floor = test.get_problem(3).rack.floor
    input = test.get_problem(3).input
    output = test.get_problem(3).output



    ts = action()
    sm = nextstate.simul()

    # rs = [8, 20, 10, 5, 7, 20, -1, 8, -1, -1, 18, 13, 10, 5, 13, 1, 4, -1, 14, 1, 14, 0, 4, 7, 13, 10, 12, 9, 14, 22, 10, 1, 15, 13, 15, -1, -1, 12, 16, -1, 6, 7, 17, 25, 9, 15, -1, 8, 17, -1, 0, 4, 19, 12, 17, 4, -1, 13, 20, 6, 4, -1, 17, 5, 8, 11, 9, -1, -1, 10, 13, 6, 17, 17, -1, 17, -1, 9, -1, 21, 5, 15, 5, 2, 20, 4, -1, -1, 12, 21, 7, 2, 4, 19, -1, -1, -1, 4, 13, 16, 17, 3, 6, 5, 13, 18, 6, -1, -1, 0, 7, 15, 8, 9, 10, 5, 9, 2, 18, 13, 18, 17, 19, 5, 13, 5, 13, 4, -1, 2, 17, 6, 5, 7, 20, 15, -1, -1, 6, 5, 15, 19, 20, 15, 8, -1, -1, 23, 5, 5, 19, 15, 2, 9, 5, 16, 16, -1, -1, 1, 2, 13, 18, 15, 13, 11, -1, 7, 9, -1, 2, 4, 19, 20, 16, 16, -1, 5, -1, -1, 13, 4, 20, 2, 19, 10, -1, 17, -1, -1, 4, 22, 10, 9, 5, -1, -1, 14, 17, 20]
    # input = [19,8]
    # output = [11,11]
    # ts.dijk(rs,column,floor,input,output)

    print rs
    for cycle in range(len(input)/2):
        print cycle
        inputs = input[(cycle+1)*2-2:(cycle+1)*2]
        outputs = output[(cycle + 1) * 2 - 2:(cycle + 1) * 2]
        print inputs
        print outputs
        a,b = ts.dijk(rs, column, floor,inputs, outputs)
        rs = sm.change_rs(rs, column, floor, a)
        print rs






    # # rs0 = test.get_problem(2).rack.status
    # rs1 = test.get_problem(2).rack.status
    # # da = rs1.count(17)
    # # ea = 0
    # # print da
    # # rs2 = test.get_problem(3).rack.status
    # # rs3 = test.get_problem(3).rack.status
    # # rs4 = test.get_problem(3).rack.status
    # # rs5 = test.get_problem(3).rack.status
    # # rs6 = test.get_problem(3).rack.status
    # # rs7 = test.get_problem(3).rack.status
    #
    # # vr = visualize_rack.visualize()
    # # vr.visual_rack(rs,column,floor)
    #
    # for cycle in range(len(input)/2):
    #     print cycle
    #     inputs = input[(cycle+1)*2-2:(cycle+1)*2]
    #     outputs = output[(cycle + 1) * 2 - 2:(cycle + 1) * 2]
    #     # da += inputs.count(17)
    #     # ea += outputs.count(17)
    #     # print da, ea
    #     # a,b = ts.dijk_srsr_with_abc_a(rs0,column,floor,inputs,outputs)
    #     # print a.type, a.loc
    #     c,d = ts.dijk_srsr_with_abc_b(rs1,column,floor,inputs,outputs)
    #     print c.type, c.loc
    #     # e,f = ts.dijk_srsr_faster_one(rs2,column,floor,inputs,outputs)
    #     # print e.type, e.loc
    #     # g,h = ts.dijk_srsr_density_test_fixed_output(rs3,column,floor,inputs,outputs)
    #     # print g.type, g.loc
    #     # i,j = ts.dijk_srsr_density(rs4,column,floor,inputs,outputs,0)
    #     # print i.type, i.loc
    #     # l,m = ts.dijk_srsr_density(rs5,column,floor,inputs,outputs,1)
    #     # print l.type, l.loc
    #     # n,o = ts.dijk_srsr_density(rs6,column,floor,inputs,outputs,2)
    #     # print n.type, n.loc
    #     # p,q = ts.dijk_srsr_density(rs7,column,floor,inputs,outputs,3)
    #     # print p.type, p.loc
    #     # cycletime0 += b
    #     cycletime1 += d
    #     # cycletime2 += f
    #     # cycletime3 += h
    #     # cycletime4 += j
    #     # cycletime5 += m
    #     # cycletime6 += o
    #     # cycletime7 += q
    #     # rs0 = sm.change_rs(rs0,column,floor,a)
    #     rs1 = sm.change_rs(rs1,column,floor,c)
    #     print rs1
    #     # rs2 = sm.change_rs(rs2,column,floor,e)
    #     # rs3 = sm.change_rs(rs3,column,floor,g)
    #     # rs4 = sm.change_rs(rs4,column,floor,i)
    #     # rs5 = sm.change_rs(rs5,column,floor,l)
    #     # rs6 = sm.change_rs(rs6,column,floor,n)
    #     # rs7 = sm.change_rs(rs7,column,floor,p)
    #     #
    # # print "abc large > few :" + str(cycletime0)
    # # print "abc few > large :" + str(cycletime1)
    # # print "dijk_srsr_faster_one :" + str(cycletime2)
    # # print "dijk_srsr fixed retrieval(large>few) :" + str(cycletime3)
    # # print "dijk_srsr_density_0 :" + str(cycletime4)
    # # print "dijk_srsr_density_1 :" + str(cycletime5)
    # # print "dijk_srsr_density_2 :" + str(cycletime6)
    # # print "dijk_srsr_density_3 :" + str(cycletime7)
    # # vr.visual_rack(rs0, column, floor)
    # # vr.visual_rack(rs1, column, floor)
    # # vr.visual_rack(rs2, column, floor)
    # # vr.visual_rack(rs3, column, floor)
    # # vr.visual_rack(rs4, column, floor)
    # # vr.visual_rack(rs5, column, floor)
    # # vr.visual_rack(rs6, column, floor)
    # # vr.visual_rack(rs7, column, floor)
    #
    #
    #
    # #ts.abc_action_SSRR(rs,column,floor,input,output)

