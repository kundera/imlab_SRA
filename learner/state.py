class state:

    def get_storage_binary(self, rack_status):
        result = ''
        for i in rack_status.split(','):
            if i == '-1':
                result += '0'
            else:
                result += '1'
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
                        result += '0'

                    elif j == item_type:
                        result += '1'
                    else:
                        result += '2'
                results.append(result)

        return results

    def get_retrieval_binary(self, rack_status, solution):
        results = []
        for i in solution.split('/'):
            if i[len(i) - 1] == 'R':
                result = ''
                item_type = i.split('_')[1]
                for j in rack_status.split(','):
                    if j == item_type:
                        result += '1'
                    else:
                        result += '0'
                results.append(result)

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
                    result += str(retrieval.index(k)+1)
                    boolean = False
                    break
            if boolean:
                 result += '0'
        return result

test = state()
print test.get_retrieval_ternary('319,189,716,379', '0,1,0_319_S/1,15,2_189_R/1,15,2_716_S/1,2,5_379_R')