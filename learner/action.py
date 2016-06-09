from problemIO import problemreader
import networkx as nx
import math
import solution
from simulator import nextstate
from simulator import visualize_rack
from collections import Counter
import matplotlib.pyplot as plt


class action(object):

    yspeed = 2.
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
                if float(data) == 0:
                    G.remove_edge('%s' % n, '%s' % nbr)

        #print G.node
        #print G.edge

        #print 'end'

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'S', 'R', 'R']
        #nx.draw_networkx(G ,arrows=True,with_labels=True)
        #plt.show()
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
                if data == 0.0:
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
                    if loca3[0] != loca2[0] and item3 == -1 and loca3[1:3] == loca2[1:3] :
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                    elif loca3 == loca2:
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

        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 3 and data1 == data3 :
                    if data1[0] == 0:
                        data1[0] = 1
                        if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True :
                            G.remove_edge('%s_r1' % data1, '%s_s2' % data3)
                    elif data1[0] == 1:
                        data1[0] = 0
                        if G.has_edge('%s_r1' % data1, '%s_s2' % data3) == True :
                            G.remove_edge('%s_r1' % data1, '%s_s2' % data3)







        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S', 'R', 'S', 'R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR1SR2', path['start']['end'], length['start']['end']
        return 'SR1SR2', path, length, self.print_dijk(G),io

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
                    if loca3[0] != loca2[0] and item3 == -1 and loca3[1:3] == loca2[1:3]:
                        G.add_node('%s_s2' % loca3, loca=loca3, phase=3)
                        G.add_edge('%s_r2' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                    elif loca3 == loca2:
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

        path = nx.dijkstra_path(G,'start','end')
        length = nx.dijkstra_path_length(G, 'start', 'end')
        io = ['S','R','S','R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR2SR1', path['start']['end'], length['start']['end']
        return 'SR2SR1', path, length, self.print_dijk(G), io

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
            io = [input[0], output[0], input[1], output[1]]
            sol = solution.solution(d1, io, e1)
            cycletime = c1
            return sol, cycletime
        elif c2 < c1:
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








if __name__ == '__main__':
    test = problemreader.ProblemReader(25)
    rs = test.get_problem(2).rack.status
    column = test.get_problem(2).rack.column
    floor = test.get_problem(2).rack.floor
    input = test.get_problem(2).input
    output = test.get_problem(2).output

    ts = action()
    sm = nextstate.simul()
    cycletime0 = 0
    cycletime1 = 0
    cycletime2 = 0
    cycletime3 = 0
    cycletime4 = 0
    cycletime5 = 0
    cycletime6 = 0
    cycletime7 = 0

    rs0 = test.get_problem(2).rack.status
    rs1 = test.get_problem(2).rack.status
    rs2 = test.get_problem(2).rack.status
    rs3 = test.get_problem(2).rack.status
    rs4 = test.get_problem(2).rack.status
    rs5 = test.get_problem(2).rack.status
    rs6 = test.get_problem(2).rack.status
    rs7 = test.get_problem(2).rack.status

    # vr = visualize_rack.visualize()
    # vr.visual_rack(rs,column,floor)

    for i in range(len(input)/2):
        inputs = input[(i+1)*2-2:(i+1)*2]
        outputs = output[(i + 1) * 2 - 2:(i + 1) * 2]
        a,b = ts.dijk_srsr_with_abc_a(rs0,column,floor,inputs,outputs)
        print a.type, a.loc
        c,d = ts.dijk_srsr_with_abc_b(rs1,column,floor,inputs,outputs)
        print c.type, c.loc
        e,f = ts.dijk_srsr_faster_one(rs2,column,floor,inputs,outputs)
        print e.type, e.loc
        g,h = ts.dijk_srsr_density_test_fixed_output(rs3,column,floor,inputs,outputs)
        print g.type, g.loc
        i,j = ts.dijk_srsr_density(rs4,column,floor,inputs,outputs,0)
        print i.type, i.loc
        l,m = ts.dijk_srsr_density(rs5,column,floor,inputs,outputs,1)
        print l.type, l.loc
        n,o = ts.dijk_srsr_density(rs6,column,floor,inputs,outputs,2)
        print n.type, n.loc
        p,q = ts.dijk_srsr_density(rs7,column,floor,inputs,outputs,3)
        print p.type, p.loc
        cycletime0 += b
        cycletime1 += d
        cycletime2 += f
        cycletime3 += h
        cycletime4 += j
        cycletime5 += m
        cycletime6 += o
        cycletime7 += q
        rs0 = sm.change_rs(rs0,column,floor,a)
        rs1 = sm.change_rs(rs1,column,floor,c)
        rs2 = sm.change_rs(rs2,column,floor,e)
        rs3 = sm.change_rs(rs3,column,floor,g)
        rs4 = sm.change_rs(rs4,column,floor,i)
        rs5 = sm.change_rs(rs5,column,floor,l)
        rs6 = sm.change_rs(rs6,column,floor,n)
        rs7 = sm.change_rs(rs7,column,floor,p)

    print "abc large > few :" + str(cycletime0)
    print "abc few > large :" + str(cycletime1)
    print "dijk_srsr_faster_one :" + str(cycletime2)
    print "dijk_srsr fixed retrieval(large>few) :" + str(cycletime3)
    print "dijk_srsr_density_0 :" + str(cycletime4)
    print "dijk_srsr_density_1 :" + str(cycletime5)
    print "dijk_srsr_density_2 :" + str(cycletime6)
    print "dijk_srsr_density_3 :" + str(cycletime7)
    # vr.visual_rack(rs0, column, floor)
    # vr.visual_rack(rs1, column, floor)
    # vr.visual_rack(rs2, column, floor)
    # vr.visual_rack(rs3, column, floor)
    # vr.visual_rack(rs4, column, floor)
    # vr.visual_rack(rs5, column, floor)
    # vr.visual_rack(rs6, column, floor)
    # vr.visual_rack(rs7, column, floor)



    #ts.abc_action_SSRR(rs,column,floor,input,output)

