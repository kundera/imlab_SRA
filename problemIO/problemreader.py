import MySQLdb
import problem

class ProblemReader:

    # DB Configuration
    DBAdress = 'imlab-ws2.snu.ac.kr'
    DBName = 'ASRS'
    DBID = 'ioasrs'
    DBPassward = '1wjdqhruddud'

    def __init__(self, table_idx, problem_idx):
        self.table_idx = table_idx
        self.problem_idx = problem_idx

    def get_problem(self):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfigNew WHERE idx = '+str(self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        p = problem.Problem(row[0], row[1], row[2], row[3], row[4], row[5])

        sql = 'SELECT rack, input, output FROM problemSet_c'+str(self.table_idx)+ ' WHERE idx = '+str(self.problem_idx)
        cur.execute(sql)
        #for i in range(cur.rowcount):
        row = cur.fetchone()
        p.set_problem(row[0], row[1], row[2])
        con.close()
        return p

class ProblemWithSolutionReader(ProblemReader):

    DBName = 'ASRS.solver'

    def get_problem_with_solution(self):
        con = MySQLdb.connect(self.DBAdress, self.DBID, self.DBPassward, self.DBName)
        cur = con.cursor()
        sql = 'SELECT aisleNum, columnNum, floorNum, itemTypeNum,  requestLength, shuttleNum FROM problemConfig WHERE idx = ' + str(
            self.table_idx)
        cur.execute(sql)
        row = cur.fetchone()
        pws = problem.ProblemWithSolution(row[0], row[1], row[2], row[3], row[4], row[5])

        sql = 'SELECT rack, input, output, NN_sol, RNN_sol FROM problemSet_c' + str(self.table_idx) + ' WHERE idx = ' + str(
            self.problem_idx)
        cur.execute(sql)
        # for i in range(cur.rowcount):
        row = cur.fetchone()
        pws.set_problem_with_solution(row[0], row[1], row[2], row[3], row[4])
        con.close()
        return pws

if __name__ == '__main__':
    test = ProblemWithSolutionReader(2, 3)
    print test.get_problem_with_solution().output
