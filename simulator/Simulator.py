from problemIO import problemreader

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


#============================== unused parameter =========================================
hv = 1 # horizontal velocity of crane
vv = 4 # vertical velocity of crane
one_cycle_act = 4 # the number of one cycle action


#============================== adjusting rs data type =========================================
def adjust_rs(rs1) :

    rs1 = rs1.replace(" ","")
    rs1 = rs1.split(",")
    for i in range(len(rs1)):
        rs1[i] = int(rs1[i])


    print rs1
    return rs1

#============================== adjusting the order data type =========================================
def adjust_order(order_raw):
    dividing_order = order_raw.split("/") # splitting by '/' and making a list

    for i in range(len(dividing_order)):
        dividing_loc.append(dividing_order[i].split("_"))
    for j in range(len(dividing_loc)):
        ordered_rackloc.append(dividing_loc[j][0])
    for i in range(len(ordered_rackloc)):
        ordered_rackloc2.append(ordered_rackloc[i].split(","))

    for item in range(len(dividing_loc)):
        ordered_item.append(dividing_loc[item][1])

    for action in range(len(dividing_loc)):
        ordered_action.append(dividing_loc[action][2])

    for element in range(len(ordered_rackloc2)): # changing ijk data type of rack location (str -> int  )
       for ijk in range(len(ordered_rackloc2[element])):
          ordered_rackloc2[element][ijk] = int(ordered_rackloc2[element][ijk])

    for i in range(len(ordered_item)):
        ordered_item2.append(int(ordered_item[i]))


    print ordered_rackloc2
    print ordered_action
    print ordered_item2
    return ordered_item2, ordered_action, ordered_rackloc2


#============================== Changing Rack Status by Action =========================================
def change_rs(rs1,order_raw):
    rs2 = adjust_rs(rs1)
    ordered_item2, ordered_action, ordered_rackloc2 = adjust_order(order_raw)


    rs_file = open("RackStatus(%s, %s).txt" % (tidx, pidx),'w')
    for action in range(len(ordered_action)):
        loca = (rack_size_h * rack_size_v * ordered_rackloc2[action][0]) + (rack_size_v * ordered_rackloc2[action][1]) + \
               ordered_rackloc2[action][2]

        if action % one_cycle_act == 0 : #one_cylce_act = 4

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
    print rs1
    print rs2


change_rs(rs1,order_raw)