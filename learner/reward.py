class reward:
    ySpeed = 2.5
    zSpeed = 0.6666667

    def get_maxtime(self, columnNum, floorNum, shuttleNum):
        return (shuttleNum * 2 + 1) * self.get_time('0,0,0', '0,' + str(columnNum-1) + ',' + str(floorNum-1))

    def get_cycletime(self, solution):
        cycletime = 0.0
        for i in range(len(solution.split('/'))):
            if i == 0:
                cycletime += self.get_time('0,0,0', solution.split('/')[i].split('_')[0])
            else:
                cycletime += self.get_time(solution.split('/')[i].split('_')[0], solution.split('/')[i-1].split('_')[0])

        cycletime += self.get_time('0,0,0', solution.split('/')[len(solution.split('/'))-1].split('_')[0])
        return cycletime

    def get_time(self, start, end):
        return max(abs((float(start.split(',')[1]) - float(end.split(',')[1])) / self.ySpeed),
                   abs((float(start.split(',')[2]) - float(end.split(',')[2])) / self.zSpeed))

test = reward()
print test.get_cycletime('0,1,0_319_S/1,15,2_189_R')