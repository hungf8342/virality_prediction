# This file takes a graph file and shuffles it
# The format for a graph file is:
#    number_of_nodes number_of_edges
#    edge_1_node_1 edge_1_node_2
#    edge_2_node_1 edge_2_node_2
#    edge_3_node_1 edge_3_node_2
#        ...           ...
#
# The nodes in the graph file need to be indexed
# from 0 to (number_of_nodes - 1)


import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import networkx as nx


def main():
    gDat = open("orig_graphs/socfb-Caltech36.mtx", 'rb')
    
    # Read the node and edge numbers
    firstLine = gDat.readline().split()
    
    # Load the rest of the data into a networkx network
    graph = nx.read_edgelist(gDat)

    for i in range(100):
        
        # Shuffle the network
        nx.double_edge_swap(graph, nswap=20000, max_tries=100000)
        
        # Load the network into another file with proper formatting
        filename = "graphs/socfb_cal_" + str(i) + ".dat"
        g_filename = "global_graphs/socfb_cal_" + str(i) + ".dat"
        output = [firstLine]
        g_output = []
        for line in nx.generate_edgelist(graph):
            vals = line.split()
            output.append([int(vals[0]), int(vals[1])])
            g_output.append([int(vals[0]), int(vals[1])])

        np.savetxt(open(filename, "wb"), output, fmt="%s")
        np.savetxt(open(g_filename, "wb"), g_output, delimiter='\t', fmt="%s")
        print(filename)

main()
