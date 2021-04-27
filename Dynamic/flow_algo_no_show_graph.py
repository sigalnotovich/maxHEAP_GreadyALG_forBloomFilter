# Ford-Fulkerson Algorithm

# find path by using BFS
import numpy

from flow_algorithm_no_show_graph.new_matrix import new_matrix
import networkx as nx
import matplotlib.pyplot as plt

NUM_OF_BITS_IN_BLOOM_FILTER = 2048

def dfs(C, F, s, t):
    stack = [s]
    paths = {s: []}
    if s == t:
        return paths[s]
    while (stack):
        u = stack.pop()
        for v in range(len(C)):
            if (C[u][v] - F[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                print
                paths
                if v == t:
                    return paths[v]
                stack.append(v)
    return None


def max_flow(C, s, t, num_trx_in_current_block):
    n = len(C)  # C is the capacity matrix
    F = [[0] * n for i in range(n)]
    path = dfs(C, F, s, t)
    while path != None:
        flow = min(C[u][v] - F[u][v] for u, v in path)
        for u, v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = dfs(C, F, s, t)
    # print_selected_trx:
    sum_of_all = 0
    sum3 = 0
    for i in range(1, num_trx_in_current_block + 1):
        row = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + i
        col = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + num_trx_in_current_block + 1

        if F[row][col] == 3:
            sum_of_all += 3
            sum3 +=3
            print("transaction with indexs {0} added to the block with ---3---".format(i))
        if F[row][col] == 2:
            sum_of_all += 2
            #print("transaction with indexs {0} added to the block with ---2---".format(i))
        if F[row][col] == 1:
            sum_of_all += 1
            #print("transaction with indexs {0} added to the block with ---1---".format(i))
    print("sum of trx that have 3 flow: " ,sum3/3)
    print("sum of all is: ", sum_of_all)

    #from trx1 to trxN :
        #if F[trx1][t] == 3:
            #print (indx of trx1)
    return sum(F[s][i] for i in range(n))

# def print_selected_trx():


# make a capacity graph
# to: s  o  p  q  r  t
C = [[0, 3, 3, 0, 0, 0],  # from s
     [0, 0, 2, 3, 0, 0],  # from o
     [0, 0, 0, 0, 2, 0],  # from p
     [0, 0, 0, 0, 4, 2],  # from q
     [0, 0, 0, 0, 0, 2],  # from r
     [0, 0, 0, 0, 0, 0]]  # from t



# def print_graph(C_new):
    # C_nuw_numpy = numpy.array(C_new)
    # D = nx.DiGraph(C_nuw_numpy) #networkX graph
    # nx.draw(D)
    #plt.draw(C_nuw_numpy)

#csv = "block_num_11838934.csv" #todo
csv_file = "merged_trxes_1112trx.csv"
number_of_trx_in_new_block = float('inf')
C_new, num_trx_in_current_block, arraylen = new_matrix(csv_file, number_of_trx_in_new_block)
# print_graph(C_new)

source = 0  # A
sink = arraylen - 1 # F
max_flow_value = max_flow(C_new, source, sink, num_trx_in_current_block)

# source= 0
# sink = 5
# max_flow_value = max_flow(C, source, sink)
print("Ford-Fulkerson algorithm")
print("max_flow_value is: ", max_flow_value)

input()