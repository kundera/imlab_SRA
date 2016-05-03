from problemIO import problemreader


class simul(object):
    #============================== used parameter =========================================
    tidx = 6 # tableidx in DB
    pidx = 1 # problemidx in DB
    testset = problemreader.ProblemWithSolutionReader(tidx, pidx) # get test set from DB
    rs1 = testset.get_problem_with_solution().rack # rack status
    order_raw = testset.get_problem_with_solution().NN_sol # given order
    order_loc = [] # repository of given order's location
    rack_size_h = testset.get_problem_with_solution().columnNum # the number of column
    rack_size_v = testset.get_problem_with_solution().floorNum # the number of floor

    dividing_loc = [] # repository of given order's dividing location
    ordered_rackloc = []  # ex) [[1, 1, 1], [1, 0, 2], [1, 2, 4], [1, 1, 2], [1, 2, 1], [1, 0, 1], [1, 2, 2], [1, 1, 3]]
    ordered_rackloc2 = []
    ordered_item = []  # ex) ['21', '22', '23', '20', '27', '28', '25', '26']
    ordered_item2 = []
    ordered_action = []  # ex) ['S', 'R', 'R', 'S', 'S', 'S', 'R', 'R']
    one_cycle_act = 4 # the number of one cycle action


    #============================== unused parameter =========================================
    hv = 1 # horizontal velocity of crane
    vv = 4 # vertical velocity of crane


    #============================== adjusting rs data type =========================================
    def adjust_rs(self, rs1) :

        rs1 = rs1.replace(" ","")
        rs1 = rs1.split(",")
        for i in range(len(rs1)):
            rs1[i] = int(rs1[i])


        #print rs1
        return rs1

    #============================== adjusting the order data type =========================================
    def adjust_order(self, order_raw):
        dividing_order = order_raw.split("/") # splitting by '/' and making a list

        for i in range(len(dividing_order)):
            simul.dividing_loc.append(dividing_order[i].split("_"))
        for j in range(len(simul.dividing_loc)):
            simul.ordered_rackloc.append(simul.dividing_loc[j][0])
        for i in range(len(simul.ordered_rackloc)):
            simul.ordered_rackloc2.append(simul.ordered_rackloc[i].split(","))

        for item in range(len(simul.dividing_loc)):
            simul.ordered_item.append(simul.dividing_loc[item][1])

        for action in range(len(simul.dividing_loc)):
            simul.ordered_action.append(simul.dividing_loc[action][2])

        for element in range(len(simul.ordered_rackloc2)): # changing ijk data type of rack location (str -> int  )
           for ijk in range(len(simul.ordered_rackloc2[element])):
               simul.ordered_rackloc2[element][ijk] = int(simul.ordered_rackloc2[element][ijk])

        for i in range(len(simul.ordered_item)):
            simul.ordered_item2.append(int(simul.ordered_item[i]))


        #print simul.ordered_rackloc2
        #print simul.ordered_action
        #print simul.ordered_item2
        return simul.ordered_item2, simul.ordered_action, simul.ordered_rackloc2


    #============================== Changing Rack Status by Action =========================================
    def change_rs(self, rs1, order_raw):
        rs2 = self.adjust_rs(rs1)
        ordered_item2, ordered_action, ordered_rackloc2 = self.adjust_order(order_raw)


        rs_file = open("RackStatus(%s, %s).txt" % (simul.tidx, simul.pidx),'w')
        for action in range(len(ordered_action)):
            loca = (simul.rack_size_h * simul.rack_size_v * ordered_rackloc2[action][0]) + (simul.rack_size_v * ordered_rackloc2[action][1]) + \
                   ordered_rackloc2[action][2]

            if action % simul.one_cycle_act == 0 : #one_cylce_act = 4

                rs_file.write(str(rs2) + "\n")

                if ordered_action[action] == 'S':
                    rs2[loca] = ordered_item2[action]

                elif ordered_action[action] == 'R':
                    rs2[loca] = -1


            else:
                if ordered_action[action] == 'S':
                    rs2[loca] = ordered_item2[action]

                elif ordered_action[action] == 'R':
                    rs2[loca] = -1

        rs_file.close()
        #print rs1
        #print rs2


if __name__ == '__main__':
    test = simul()
    a = test.rs1
    b = test.order_raw
    test.change_rs(a, b)


from problemIO import problemreader


class simul(object):
    #============================== used parameter =========================================
    tidx = 3 # tableidx in DB
    pidx = 1 # problemidx in DB
    testset = problemreader.ProblemWithSolutionReader(tidx, pidx) # get test set from DB
    rs1 = testset.get_problem_with_solution().rack # rack status
    order_raw = testset.get_problem_with_solution().NN_sol # given order
    order_loc = [] # repository of given order's location
    rack_size_h = testset.get_problem_with_solution().columnNum # the number of column
    rack_size_v = testset.get_problem_with_solution().floorNum # the number of floor

    dividing_loc = [] # repository of given order's dividing location
    ordered_rackloc = []  # ex) [[1, 1, 1], [1, 0, 2], [1, 2, 4], [1, 1, 2], [1, 2, 1], [1, 0, 1], [1, 2, 2], [1, 1, 3]]
    ordered_rackloc2 = []
    ordered_item = []  # ex) ['21', '22', '23', '20', '27', '28', '25', '26']
    ordered_item2 = []
    ordered_action = []  # ex) ['S', 'R', 'R', 'S', 'S', 'S', 'R', 'R']
    one_cycle_act = 4 # the number of one cycle action


    #============================== unused parameter =========================================
    hv = 1 # horizontal velocity of crane
    vv = 4 # vertical velocity of crane


    #============================== adjusting rs data type =========================================
    def adjust_rs(self, rs1) :

        rs1 = rs1.replace(" ","")
        rs1 = rs1.split(",")
        #for i in range(len(rs1)):
        #    rs1[i] = int(rs1[i])


        #print rs1
        return rs1

    #============================== adjusting the order data type =========================================
    def adjust_order(self, order_raw):
        dividing_order = order_raw.split("/") # splitting by '/' and making a list

        for i in range(len(dividing_order)):
            simul.dividing_loc.append(dividing_order[i].split("_"))
        for j in range(len(simul.dividing_loc)):
            simul.ordered_rackloc.append(simul.dividing_loc[j][0])
        for i in range(len(simul.ordered_rackloc)):
            simul.ordered_rackloc2.append(simul.ordered_rackloc[i].split(","))

        for item in range(len(simul.dividing_loc)):
            simul.ordered_item.append(simul.dividing_loc[item][1])

        for action in range(len(simul.dividing_loc)):
            simul.ordered_action.append(simul.dividing_loc[action][2])

        for element in range(len(simul.ordered_rackloc2)): # changing ijk data type of rack location (str -> int  )
           for ijk in range(len(simul.ordered_rackloc2[element])):
               simul.ordered_rackloc2[element][ijk] = int(simul.ordered_rackloc2[element][ijk])

        for i in range(len(simul.ordered_item)):
            simul.ordered_item2.append(int(simul.ordered_item[i]))


        #print simul.ordered_rackloc2
        #print simul.ordered_action
        #print simul.ordered_item2
        return simul.ordered_item2, simul.ordered_action, simul.ordered_rackloc2


    #============================== Changing Rack Status by Action =========================================
    def change_rs(self, rs1, order_raw): # order_raw format : ['59','51','68','1',[1,0,0],[1,0,1],[1,0,1],[1,4,1],'S','R','S','R']
        rs2 = self.adjust_rs(rs1)
        print rs2
        rack_size_h = simul.rack_size_h
        rack_size_v = simul.rack_size_v
        one_cycle_act = simul.one_cycle_act
        #ordered_item2, ordered_action, ordered_rackloc2 = self.adjust_order(order_raw)

        for action in range(4):
            loca = (rack_size_h * rack_size_v * order_raw[action+4][0]) + (rack_size_v * order_raw[action+4][1]) + \
                   order_raw[action+4][2]

            if action % one_cycle_act == 0 : #one_cylce_act = 4

                if order_raw[action+8] == 'S':
                    rs2[loca] = order_raw[action]

                elif order_raw[action+8] == 'R':
                    rs2[loca] = '-1'


            else:
                if order_raw[action+8] == 'S':
                    rs2[loca] = order_raw[action]

                elif order_raw[action+8] == 'R':
                    rs2[loca] = '-1'

        return rs2


if __name__ == '__main__':
    test = simul()
    a = test.rs1
    test.change_rs(a, ['59','68','51','1',[1,0,0],[1,0,1],[1,0,1],[1,4,1],'S','S','R','R'])
