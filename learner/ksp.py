import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
import Queue
import math
import time


from problemIO import problemreader
import solution

class KSP():

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

    def adjust_rs(self, rs1):
        rs1 = rs1.replace(" ", "")
        rs1 = rs1.split(",")

        return rs1

    def adjust_list(self, lst):
        for i, j in enumerate(lst):
            for k in range(len(j)):
                lst[i][k] = int(lst[i][k])
        return lst

    def print_dijk(self, path):
        sol_of_loca = path[1][:-3] + "/" + path[2][:-3] + "/" \
                      + path[3][:-3] + "/" + path[4][:-3]
        sol_of_loca = sol_of_loca.replace("[", "")
        sol_of_loca = sol_of_loca.replace("]", "")
        sol_of_loca = sol_of_loca.replace(" ", "")
        list_sol_of_loca = sol_of_loca.split("/")
        list_sol_of_loca = [x.split(',') for x in list_sol_of_loca]
        list_sol_of_loca = self.adjust_list(list_sol_of_loca)
        return list_sol_of_loca

    # Yen's algorithm for K-shortest paths in an edge-weighted graph G (undirected or directed)

    # Cost/weight of path p in graph G
    def pweight(self, G, p):
        w = 0
        for i in range(len(p) - 1):
            w += G[p[i]][p[i + 1]]['weight']
        return w

    # Copy edge (a,z) of G, remove it, and return the copy.
    # This can become expensive!
    def cprm(self, G, a, z):
        ec = deepcopy(G[a][z])
        G.remove_edge(a, z)
        return a, z, ec

    # Copy node n of G, remove it, and return the copy.
    # This can become expensive!
    def cprmnode(self, G, n):
        ec = deepcopy(G[n])
        G.remove_node(n)
        return n, ec

    # K shortest paths in G from 'source' to 'target'
    def yen(self, G, source, target, itr):
        # First shortest path from the source to the target
        c, p = nx.single_source_dijkstra(G, source, target)
        A = [p[target]]  # path
        A_cost = [c[target]]  # length
        B = Queue.PriorityQueue()

        # for k in range(1, K):
        k = 1
        while itr > k:
            for i in range(len(A[k - 1]) - 1):
                # Spur node ranges over the (k-1)-shortest path minus its last node:
                sn = A[k - 1][i]
                if sn[-2:] == 'r2':
                    break
                # Root path: from the source to the spur node of the (k-1)-shortest path
                rp = A[k - 1][:i]

                # We store the removed edges
                removed_edges = []
                removed_root_edges = []
                removed_root_nodes = []
                # Remove the root paths
                for j in range(len(rp) - 1):

                    extra_edges = []
                    extra_edges = G.edges(rp[j])

                    for eg in extra_edges:
                        src = eg[0]
                        tgt = eg[1]

                        removed_root_edges.append(self.cprm(G, src, tgt))

                    removed_root_nodes.append(self.cprmnode(G, rp[j]))

                    # G.remove_node(rp[j])

                if len(rp) > 0 and sn != target:

                    extra_edges = []
                    extra_edges = G.edges(rp[len(rp) - 1])

                    for eg in extra_edges:
                        src = eg[0]
                        tgt = eg[1]
                        removed_root_edges.append(self.cprm(G, src, tgt))

                    removed_root_nodes.append(self.cprmnode(G, rp[len(rp) - 1]))

                # Remove the edges that are part of the already-found k-shortest paths
                # which share the same extended root path
                erp = A[k - 1][:i + 1]  # extended root path
                for p in A:
                    if erp == p[:i + 1] and G.has_edge(p[i], p[i + 1]):
                        removed_edges.append(self.cprm(G, p[i], p[i + 1]))
                # The spur path

                DONE = 0
                try:
                    (csp, sp) = nx.single_source_dijkstra(G, sn, target)
                    sp = sp[target]
                    csp = csp[target]

                except:
                    # there is no spur path if sn is not connected to the target
                    sp = []
                    csp = None
                    DONE = 1
                    # return (A, A_cost)
                if len(sp) > 0:
                    # The potential k-th shortest path (the root path may be empty)
                    pk = rp + sp

                    for nd in removed_root_nodes:
                        G.add_node(*nd)

                    for re in removed_root_edges:
                        G.add_edge(*re)
                    cpk = self.pweight(G, pk)
                    # Add the potential k-shortest path to the heap
                    B.put((cpk, pk))
                # Add back the edges that were removed
                if len(sp) == 0:
                    for nd in removed_root_nodes:
                        G.add_node(*nd)
                    for re in removed_root_edges:
                        G.add_edge(*re)
                for re in removed_edges:
                    G.add_edge(*re)
                for nd in removed_root_nodes:
                    G.add_node(*nd)

            if B.empty():
                print 'There are only', k, 'shortest paths for this pair'
                break
            # The shortest path in B that is not already in A is the new k-th shortest path
            while not B.empty():
                cost, path = B.get()
                if path not in A:
                    if path[2][0:-3] == path[3][0:-3]:
                        A.append(path)
                        # print k, path
                        A_cost.append(cost)

                        k += 1
                        break

        return A, A_cost

    def k_shortest_path(self, rs, column, floor, inputs, outputs, itr):

        G = nx.Graph()

        G.add_node('start', loca=[0, 0, 0], phase=0)
        G.add_node('end', loca=[0, 0, 0], phase=5)
        init_loca = [0, 0, 0]
        end_loca = [0, 0, 0]
        rack = rs
        size_h = column
        size_v = floor

        # create S1
        for a, item1 in enumerate(rack):
            if item1 == -1:
                loca1 = self.loca_calculate(a, size_h, size_v)
                G.add_node('%s_s1' % loca1, loca=loca1, phase=1)
                G.add_edge('start', '%s_s1' % loca1, weight=self.get_time(init_loca, loca1))

        # create R1
        for b, item2 in enumerate(rack):
            if item2 == outputs[0]:
                loca2 = self.loca_calculate(b, size_h, size_v)
                G.add_node('%s_r1' % loca2, loca=loca2, phase=2)
                # create S2
                G.add_node('%s_s2' % loca2, loca=loca2, phase=3)
                G.add_edge('%s_r1' % loca2, '%s_s2' % loca2, weight=self.get_time(loca2, loca2))

        # connect node S1-R1
        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 1 and data4 == 2:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # create R2
        for d, item4 in enumerate(rack):
            if item4 == outputs[1]:
                loca4 = self.loca_calculate(d, size_h, size_v)
                G.add_node('%s_r2' % loca4, loca=loca4, phase=4)
                G.add_edge('%s_r2' % loca4, 'end', weight=self.get_time(loca4, end_loca))

        # connect node S2-R2
        for a, d in G.nodes_iter(data=True):
            data1 = d['loca']
            data2 = d['phase']
            for b, e in G.nodes_iter(data=True):
                data3 = e['loca']
                data4 = e['phase']
                if data2 == 3 and data4 == 4 and data1 != data3:
                    G.add_edge(a, b, weight=self.get_time(data1, data3))

        # make k paths
        k_path, path_costs = self.yen(G, 'start', 'end', itr)

        io = ['S', 'R', 'S', 'R']
        item = [inputs[0], outputs[0], inputs[1], outputs[1]]
        sols = []

        # make array of solutions
        for temp in range(itr):
            path = self.print_dijk(k_path[temp])
            sol = solution.solution(path, item, io)
            sols.append(sol)

        return sols, path_costs

if __name__ == '__main__':
    probnum = 28
    pronum = 2
    test = problemreader.ProblemReader(probnum)
    rs = test.get_problem(pronum).rack.status
    column = test.get_problem(pronum).rack.column
    floor = test.get_problem(pronum).rack.floor
    input = test.get_problem(pronum).input
    output = test.get_problem(pronum).output

    inputs = input[0:2]
    outputs = output[0:2]

    ksp = KSP()
    k = 20
    k_sols, k_times = ksp.k_shortest_path(rs, column, floor, inputs, outputs, k)
    for i in range(k):
        sol = k_sols[i]
        print sol.loc, sol.oper, sol.type, k_times[i]
    print '-------------------------'