from problemIO import problemreader



class simul(object):


    def change_rs(self, tidx, pidx, order_raw):  # order_raw format : ['59','51','68','1',[1,0,0],[1,0,1],[1,0,1],[1,4,1],'S','R','S','R']
        test = problemreader.ProblemReader(tidx)
        rs2 = test.get_problems(pidx)[pidx - 1].rack.status
        rack_size_h = test.get_problems(pidx)[pidx - 1].rack.column
        rack_size_v = test.get_problems(pidx)[pidx - 1].rack.floor
        # rs2 = self.adjust_rs(rs1)

        # rack_size_h = simul.rack_size_h
        # rack_size_v = simul.rack_size_v
        one_cycle_act = 4
        # ordered_item2, ordered_action, ordered_rackloc2 = self.adjust_order(order_raw)

        for action in range(one_cycle_act):
            loca = (rack_size_h * rack_size_v * order_raw[action + 1][0]) + (rack_size_v * order_raw[action + 1][1]) + \
                   order_raw[action + 1][2]

            if action % one_cycle_act == 0:  # one_cylce_act = 4
                if order_raw[5][action] == 'S':
                    rs2[loca] = order_raw[0][action]

                elif order_raw[5][action] == 'R':
                    rs2[loca] = -1


            else:
                if order_raw[5][action] == 'S':
                    rs2[loca] = order_raw[0][action]

                elif order_raw[5][action] == 'R':
                    rs2[loca] = -1

        return rs2


if __name__ == '__main__':
    test = simul()

    print test.change_rs(2, 1, [[59, 68, 13, 15], [0, 0, 2], [0, 0, 3], [0, 0, 0], [0, 0, 1], ['S', 'S', 'R', 'R']])
