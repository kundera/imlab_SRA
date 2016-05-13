import MySQLdb
from collections import deque
import reward

class OBSfromDB(object):
    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'

    def __init__(self, table_idx):
        self.table_idx = table_idx
        self._observations = deque()


    def get_obs(self, no_obs):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()

        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfig WHERE idx = ' + str(
            self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        a0, a1, a2, a3, a4, a5 = row[0], row[1], row[2], row[3], row[4], row[5]

        sql = 'SELECT state, action, cycletime, nextstate FROM '+str(self.table_idx)+ ' LIMIT = '+str(no_obs)
        cur.execute(sql)
        for i in range(cur.rowcount):
            row = cur.fetchone()
            if terminal:
                self._observations.append((row[0], row[1], row[2] / reward.reward().get_maxtime(clm, flr, sht), row[3], True))
            else:
                self._observations.append((row[0], row[1], row[2] / reward.reward().get_maxtime(clm, flr, sht), row[3], False))
        con.close()


if __name__ == '__main__':
    obs = OBSfromDB()
    obs.get_obs._observations