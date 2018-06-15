import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import networkx as nx

def main():
    graph = nx.read_edgelist("orig_graphs/karate_1.txt") 

    for i in range(10000):
        sg.shuffle(graph, 1)
        filename = "graphs/karate_s_" + str(i) + ".dat"
        output = [["34", "78"]]
        for line in nx.generate_edgelist(graph):
            vals = line.split()
            output.append([vals[0], vals[1]])
        np.savetxt(open(filename, "wb"), output, fmt="%s")
        print(filename)

main()
