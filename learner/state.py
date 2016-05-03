class state:

    def change_to_two_dimension(self, rack_status, columnNum, floorNum):
        rack_status = rack_status.split(", ")
        result = [[0 for col in range(columnNum)] for row in range(floorNum)]
        for row in range(floorNum):
            for col in range(columnNum):
                result[row][col] = rack_status[row*floorNum+col]
        return result

    def get_storage_binary(self, rack_status):
        result = ''
        for i in rack_status.split(','):
            if i == '-1':
                result += '0.0'
            else:
                result += '1.0'
            result += ','

        return result[0:len(result)-1]

    def get_storage_ternary(self, rack_status, solution):
        results = []
        for i in solution.split('/'):
            if i[len(i)-1] == 'S':
                result = ''
                item_type = i.split('_')[1]
                for j in rack_status.split(','):
                    if j == -1 :
                        result += '0.0'

                    elif j == item_type:
                        result += '0.5'
                    else:
                        result += '1.0'
                    result += ','
                results.append(result[0:len(result)-1])

        return results

    def get_retrieval_binary(self, rack_status, solution):
        results = []
        for i in solution.split('/'):
            if i[len(i) - 1] == 'R':
                result = ''
                item_type = i.split('_')[1]
                for j in rack_status.split(','):
                    if j == item_type:
                        result += '1.0'
                    else:
                        result += '0.0'
                    result += ','
                results.append(result[0:len(result)-1])

        return results

    def get_retrieval_ternary(self, rack_status, solution):
        result = ''
        retrieval = []
        for i in solution.split('/'):
            if i[len(i)-1] == 'R':
                retrieval.append(i.split('_')[1])

        for j in rack_status.split(','):
            boolean = True
            for k in retrieval:
                if j == k:
                    result += str(retrieval.index(k))+'.0'
                    boolean = False
                    break
            if boolean:
                 result += '0.5'
            result += ','
        return result[0:len(result)-1]

if __name__ == '__main__':
    test = state()
    print test.get_retrieval_binary('319,189,716,379', '0,1,0_319_S/1,15,2_189_R/1,15,2_716_S/1,2,5_379_R')