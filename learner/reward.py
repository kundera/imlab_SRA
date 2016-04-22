class reward:
    ySpeed = 2.5
    zSpeed = 0.6666667

    def get_maxtime(self, columnNum, floorNum, shuttleNum):
        return (shuttleNum * 2 + 1) * self.get_time('0,0,0', '0,' + str(columnNum-1) + ',' + str(floorNum-1))

    def get_cycletime(self, action):
        cycletime = 0.0

        for i in range(len(action)):
            if i == 0:
                cycletime += self.get_time('0,0,0', action[i])


            else:
                cycletime += self.get_time(action[i], action[i - 1])

        cycletime += self.get_time('0,0,0', action[len(action) - 1])
        return cycletime

    def get_time(self, start, end):
        return max(abs((float(start.split(',')[1]) - float(end.split(',')[1])) / self.ySpeed),
                   abs((float(start.split(',')[2]) - float(end.split(',')[2])) / self.zSpeed))
