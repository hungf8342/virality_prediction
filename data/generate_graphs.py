import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import networkx as nx

def main():
    gDat = open("orig_graphs/socfb-Caltech36.mtx", 'rb')
    firstLine = gDat.readline().split()
    graph = nx.read_edgelist(gDat)

    for i in range(100):
        nx.double_edge_swap(graph, nswap=10000, max_tries=100000)
        filename = "graphs/socfb_" + str(i) + ".dat"
        g_filename = "global_graphs/socfb_" + str(i) + ".dat"
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
