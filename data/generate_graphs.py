import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import networkx as nx

def main():
    gDat = open("orig_graphs/rt-pol_50.dat", 'rb')
    firstLine = gDat.readline().split()
    graph = nx.read_edgelist(gDat)

    for i in range(1000):
        sg.shuffle(graph, 10)
        filename = "graphs/rt-pol_s_" + str(i) + ".dat"
        output = [firstLine]
        for line in nx.generate_edgelist(graph):
            vals = line.split()
            output.append([int(vals[0]), int(vals[1])])
        np.savetxt(open(filename, "wb"), output, fmt="%s")
        print(filename)

main()
