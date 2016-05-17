import MySQLdb
from collections import deque
from learner import reward
from learner import state
import numpy as np

class OBSfromDB(object):
    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS_RL_DATA'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'

    def __init__(self, table_idx):
        self.table_idx = table_idx


    def get_obs(self, no_obs):

        observations = deque()

        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        clm = 25
        flr = 20
        sht = 2
        ACTIONS_COUNT = 4

        sql = 'SELECT rs, act, inp, outp, reward, rsprime, terminal FROM dijk_20 limit ' + str(no_obs)
        cur.execute(sql)
        for i in range(cur.rowcount):
            row = cur.fetchone()

            last_state = map(int, row[0][1:-1].split(", "))
            last_action = np.zeros([ACTIONS_COUNT])
            last_action[row[1]] = 1
            input = map(int, row[2][1:-1].split(", "))
            output = map(int, row[3][1:-1].split(", "))
            rwd = row[4] / reward.reward().get_maxtime(clm, flr, sht)
            current_state = map(int, row[5][1:-1].split(", "))
            if row[6] == 'O':
                terminal = True
            else:
                terminal = False

            rack_str1 = state.get_storage_binary(last_state)
            rack_ret1 = state.get_retrieval_binary(last_state, output)

            rack_str1 = self.change_to_two_dimension(rack_str1, clm, flr)
            rack_sr1 = rack_str1

            for i in range(len(rack_ret1)):
                rack_sr1 = np.append(rack_sr1, self.change_to_two_dimension(rack_ret1[i], clm, flr), axis=2)

            ls = rack_sr1

            rack_str2 = state.get_storage_binary(current_state)
            rack_ret2 = state.get_retrieval_binary(current_state, output)

            rack_str2 = self.change_to_two_dimension(rack_str2, clm, flr)
            rack_sr2 = rack_str2

            for i in range(len(rack_ret2)):
                rack_sr2 = np.append(rack_sr2, self.change_to_two_dimension(rack_ret2[i], clm, flr), axis=2)

            cs = rack_sr2

            observations.append((ls, last_action, rwd, cs, terminal))
        con.close()
        return observations



    def change_to_two_dimension(self, rack_status, columnNum, floorNum):
        leftrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                leftrack[clm][flr] = rack_status[clm * floorNum + flr]
        rightrack = [[0.0 for flr in range(floorNum)] for clm in range(columnNum)]
        for clm in range(columnNum):
            for flr in range(floorNum):
                rightrack[clm][flr] = rack_status[columnNum * floorNum + clm * floorNum + flr]

        result = np.append(np.reshape(np.array(leftrack), (columnNum, floorNum, 1)),
                           np.reshape(np.array(rightrack), (columnNum, floorNum, 1)), axis=2)
        return result


if __name__ == '__main__':
    obs = OBSfromDB(20)
    obs.get_obs(32)
