from problemIO import problemreader
import networkx as nx
import math
import matplotlib.pyplot as plt

class action(object):



    tidx = 2  # tableidx in DB
    pidx = 1  # problemidx in DB
    testset = problemreader.ProblemWithSolutionReader(tidx, pidx)  # get test set from DB
    rs1 = testset.get_problem_with_solution().rack
    rack_size_h = testset.get_problem_with_solution().columnNum  # the number of column
    rack_size_v = testset.get_problem_with_solution().floorNum  # the number of floor
    output = testset.get_problem_with_solution().output
    yspeed = 2.5
    zspeed = 0.6666667



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

    def dijk_ssr1r2(self, rack, size_h, size_v, outputs):# ex :outputs = ['10','18']
        G = nx.Graph()
        G.add_node('start', loca=[0, 0, 0])
        G.add_node('end', loca=[0, 0, 0])
        #rack = self.adjust_rs(rs)
        #output_list = output.replace(" ", "").split(",")
        #outputs = [output_list[i:i+2] for i in range(0, len(output_list), 2)]
        #outputs = outputs[0]
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == '-1':
                loca1 = self.loca_calculate(a, size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca,loca1))

                # create second 'S'
                for b, item2 in enumerate(rack):
                    if item2 == '-1':
                        loca2 = self.loca_calculate(b, size_h, size_v)
                        G.add_node('%s_s2' % loca2, loca=loca2)
                        G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1,loca2))

                        # remove edges weighted 0
                        for n, nbrs in G.adjacency_iter():
                            for nbr, eattr in nbrs.items():
                                data = eattr['weight']
                                if data == 0.0:
                                    G.remove_edge('%s' % n, '%s' % nbr)

                        # create 'R1R2'
                        for c, item3 in enumerate(rack):
                            loca3 = self.loca_calculate(c, size_h, size_v)
                            if item3 == outputs[0]:
                                G.add_node('%s_r1' % loca3, loca=loca3)
                                G.add_edge('%s_s2' % loca2, '%s_r1' % loca3, weight=self.get_time(loca2, loca3))

                                for d, item4 in enumerate(rack):
                                    loca4 = self.loca_calculate(d, size_h, size_v)
                                    if item4 == outputs[1]:
                                        G.add_node('%s_r2' % loca4, loca=loca4)
                                        G.add_edge('%s_r1' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

                                        # remove edges weighted 0
                                        for n, nbrs in G.adjacency_iter():
                                            for nbr, eattr in nbrs.items():
                                                data = eattr['weight']
                                                if data == 0.0:
                                                    G.remove_edge('%s' % n, '%s' % nbr)

                                        # final connect with 'end'node
                                        G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))
        # print G.node
        # print G.edge

        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        sol_of_loca = path['start']['end'][1][:-3] + "/" + path['start']['end'][2][:-3] + "/" \
                      + path['start']['end'][3][:-3] + "/" + path['start']['end'][4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        io = ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        return 'SSR1R2', path['start']['end'], length['start']['end'], list_sol_of_loca, io

    def dijk_ssr2r1(self, rack, size_h, size_v, outputs):  # ex :outputs = ['10','18']
        G = nx.Graph()
        G.add_node('start', loca=[0, 0, 0])
        G.add_node('end', loca=[0, 0, 0])
        #rack = self.adjust_rs(rs)
        #output_list = output.replace(" ", "").split(",")
        #outputs = [output_list[i:i+2] for i in range(0, len(output_list), 2)]
        #outputs = outputs[0]
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        # create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == '-1':
                loca1 = self.loca_calculate(a,size_h, size_v)
                # print loca1
                G.add_node('%s_s1' % loca1, loca=loca1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

                # create second 'S'
                for b, item2 in enumerate(rack):
                    if item2 == '-1' and a != b:
                        loca2 = self.loca_calculate(b,size_h, size_v)
                        G.add_node('%s_s2' % loca2, loca=loca2)
                        G.add_edge('%s_s1' % loca1, '%s_s2' % loca2, weight=self.get_time(loca1, loca2))

                        # create 'R2R1'
                        for c, item3 in enumerate(rack):
                            loca3 = self.loca_calculate(c,size_h, size_v)
                            if item3 == outputs[1]:
                                G.add_node('%s_r2' % loca3, loca=loca3)
                                G.add_edge('%s_s2' % loca2, '%s_r2' % loca3, weight=self.get_time(loca2, loca3))

                                for d, item4 in enumerate(rack):
                                    loca4 = self.loca_calculate(d,size_h, size_v)
                                    if item4 == outputs[0] and c != d:
                                        G.add_node('%s_r1' % loca4, loca=loca4)
                                        G.add_edge('%s_r2' % loca3, '%s_r1' % loca4, weight=self.get_time(loca3, loca4))

                                        # final connect with 'end'node
                                        G.add_edge('%s_r1' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        sol_of_loca = path['start']['end'][1][:-3] + "/" + path['start']['end'][2][:-3] + "/" \
                      + path['start']['end'][3][:-3] + "/" + path['start']['end'][4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        io= ['S', 'S', 'R', 'R']
        # nx.draw_networkx(G ,arrows=True,with_labels=True)
        # plt.show()
        # print 'SSR2R1', path['start']['end'] , length['start']['end']
        return 'SSR2R1', path['start']['end'], length['start']['end'],list_sol_of_loca,io

    def dijk_sr1sr2(self, rack,size_h, size_v, outputs): # ex :outputs = ['10','18']
        G = nx.Graph()
        G.add_node('start', loca=[0, 0, 0])
        G.add_node('end', loca=[0, 0, 0])
        #rack = self.adjust_rs(rs)
        #output_list = output.replace(" ", "").split(",")
        #outputs = [output_list[i:i + 2] for i in range(0, len(output_list), 2)]
        #outputs = outputs[0]
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        #  create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == '-1':
                loca1 = self.loca_calculate(a,size_h, size_v)
                G.add_node('%s_s1' % loca1, loca=loca1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

                # create r1
                for b, item2 in enumerate(rack):
                    loca2 = self.loca_calculate(b,size_h, size_v)
                    if item2 == outputs[0]:
                        G.add_node('%s_r1' % loca2, loca=loca2)
                        G.add_edge('%s_s1' % loca1, '%s_r1' % loca2, weight=self.get_time(loca1, loca2))

                        # create s2
                        loca3 = self.loca_calculate(b,size_h, size_v)
                        for c, item3 in enumerate(rack):
                            # check the opposite side is empty
                            loca5 = self.loca_calculate(c,size_h, size_v)
                            if c != b and loca5[0] == '-1' and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                                loca3 = loca5
                                G.add_node('%s_s2' % loca3, loca=loca3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            else:
                                G.add_node('%s_s2' % loca3, loca=loca3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                            # create r2
                            for d, item4 in enumerate(rack):
                                loca4 = self.loca_calculate(d,size_h, size_v)
                                if item4 == outputs[1] and b != d:
                                    G.add_node('%s_r2' % loca4, loca=loca4)
                                    G.add_edge('%s_s2' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

                                    # final connect with 'end'node
                                    G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        sol_of_loca = path['start']['end'][1][:-3] + "/" + path['start']['end'][2][:-3] + "/" \
                      + path['start']['end'][3][:-3]+ "/" + path['start']['end'][4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        io = ['S', 'R', 'S', 'R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR1SR2', path['start']['end'], length['start']['end']
        return 'SR1SR2', path['start']['end'], length['start']['end'], list_sol_of_loca,io

    def dijk_sr2sr1(self, rack,size_h, size_v, outputs):# ex :outputs = ['10','18']
        G = nx.Graph()
        G.add_node('start', loca=[0, 0, 0])
        G.add_node('end', loca=[0, 0, 0])
        #rack = self.adjust_rs(rs)
        #output_list = output.replace(" ", "").split(",")
        #outputs = [output_list[i:i + 2] for i in range(0, len(output_list), 2)]
        #outputs = outputs[0]
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]

        #  create first 'S'
        for a, item1 in enumerate(rack):
            if item1 == '-1':
                loca1 = self.loca_calculate(a,size_h, size_v)
                G.add_node('%s_s1' % loca1, loca=loca1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

                # create r1
                for b, item2 in enumerate(rack):
                    loca2 = self.loca_calculate(b,size_h, size_v)
                    if item2 == outputs[1]:
                        G.add_node('%s_r1' % loca2, loca=loca2)
                        G.add_edge('%s_s1' % loca1, '%s_r1' % loca2, weight=self.get_time(loca1, loca2))

                        # create s2
                        loca3 = self.loca_calculate(b,size_h, size_v)
                        for c, item5 in enumerate(rack):
                            loca5 = self.loca_calculate(c,size_h, size_v)
                            # check the opposite side is empty
                            if c != b and loca5[0] == '-1' and loca3[1] == loca5[1] and loca3[2] == loca5[2]:
                                loca3 = loca5
                                G.add_node('%s_s2' % loca3, loca=loca3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))
                            else:
                                G.add_node('%s_s2' % loca3, loca=loca3)
                                G.add_edge('%s_r1' % loca2, '%s_s2' % loca3, weight=self.get_time(loca2, loca3))

                            # create r1
                            for d, item4 in enumerate(rack):
                                loca4 = self.loca_calculate(d,size_h, size_v)
                                if item4 == outputs[0] and b != d:
                                    G.add_node('%s_r2' % loca4, loca=loca4)
                                    G.add_edge('%s_s2' % loca3, '%s_r2' % loca4, weight=self.get_time(loca3, loca4))

                                    # final connect with 'end'node
                                    G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        path = nx.all_pairs_dijkstra_path(G)
        length = nx.all_pairs_dijkstra_path_length(G)
        sol_of_loca = path['start']['end'][1][:-3] + "/" + path['start']['end'][2][:-3] + "/" \
                      + path['start']['end'][3][:-3] + "/" + path['start']['end'][4][:-3]
        sol_of_loca = sol_of_loca.replace("[","")
        sol_of_loca = sol_of_loca.replace("]","")
        sol_of_loca = sol_of_loca.replace(" ","")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        io = ['S','R','S','R']
        # nx.draw_networkx(G, arrows=True, with_labels=True)
        # plt.show()
        # print 'SR2SR1', path['start']['end'], length['start']['end']
        return 'SR2SR1', path['start']['end'], length['start']['end'], list_sol_of_loca, io

    def dijk(self,rs,size_h,size_v,input,output): # concatenate 4 solutions // input/output example : ['51', '1'] = 1 cycle outputs
        #action.tidx = tidx
        #action.pidx = pidx
        #dijk_test = problemreader.ProblemWithSolutionReader(tidx, pidx)

        #action.rs1 = dijk_test.get_problem_with_solution().rack
        #action.rack_size_h = dijk_test.get_problem_with_solution().columnNum  # the number of column
        #action.rack_size_v = dijk_test.get_problem_with_solution().floorNum  # the number of floor
        #action.output = dijk_test.get_problem_with_solution().output

        a1,b1,c1,d1,e1 = self.dijk_ssr1r2(rs,size_h, size_v, output)
        a2,b2,c2,d2,e2 = self.dijk_ssr2r1(rs,size_h, size_v, output)
        a3,b3,c3,d3,e3 = self.dijk_sr1sr2(rs,size_h, size_v, output)
        a4,b4,c4,d4,e4 = self.dijk_sr2sr1(rs,size_h, size_v, output)
        io = input + output

        if min(c1,c2,c3,c4) == c1:
            return [io[0],io[1],io[2],io[3]],d1,e1,c1
        elif min(c1,c2,c3,c4) == c2:
            return [io[0],io[1],io[3],io[2]],d2,e2,c2
        elif min(c1,c2,c3,c4) == c3:
            return [io[0],io[2],io[1],io[3]],d3,e3,c3
        elif min(c1,c2,c3,c4) == c4:
            return [io[0],io[3],io[1],io[2]],d4,e4,c4


        #print action.dijk_ssr1r2(rs,size_h, size_v, output)
        #print action.dijk_ssr2r1(rs,size_h, size_v, output)
        #print action.dijk_sr1sr2(rs,size_h, size_v, output)
        #print action.dijk_sr2sr1(rs,size_h, size_v, output)

    def dijk_idx(self, rs, size_h, size_v, input, output, idx):

        io = input + output

        if idx == 0:
            a1, b1, c1, d1, e1 = self.dijk_ssr1r2(rs, size_h, size_v, output)
            return [io[0], io[1], io[2], io[3]], d1, e1, c1
        elif idx == 1:
            a2, b2, c2, d2, e2 = self.dijk_ssr2r1(rs, size_h, size_v, output)
            return [io[0], io[1], io[3], io[2]], d2, e2, c2
        elif idx == 2:
            a3, b3, c3, d3, e3 = self.dijk_sr1sr2(rs, size_h, size_v, output)
            return [io[0], io[2], io[1], io[3]], d3, e3, c3
        elif idx == 3:
            a4, b4, c4, d4, e4 = self.dijk_sr2sr1(rs, size_h, size_v, output)
            return [io[0], io[3], io[1], io[2]], d4, e4, c4


if __name__ == '__main__':
    test = action()
    testset = problemreader.ProblemWithSolutionReader(10, 1) # config testset index
    rs = testset.get_problem_with_solution().rack
    rs = test.adjust_rs(rs)
    #print rs
    output = testset.get_problem_with_solution().output
    output_list = output.replace(" ", "").split(",")
    outputs = [output_list[i:i + 2] for i in range(0, len(output_list), 2)]
    outputs = outputs[0]

    input = testset.get_problem_with_solution().input
    input_list = input.replace(" ", "").split(",")
    inputs = [input_list[i:i + 2] for i in range(0, len(input_list), 2)]
    inputs = inputs[0]

    #print inputs, outputs

    print test.dijk_idx(rs,5,3,inputs,outputs, 0) #execute dijk function here!!!

