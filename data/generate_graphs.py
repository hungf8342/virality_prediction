import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import networkx as nx

def main():
    graph = nx.read_edgelist("orig_graphs/soc-dolphins.txt") 

    for i in range(2000):
        sg.shuffle(graph, 1)
        filename = "graphs/dolphin_s_" + str(i) + ".dat"
        output = [["62", "159"]]
        for line in nx.generate_edgelist(graph):
            vals = line.split()
            output.append([int(vals[0]) - 1, int(vals[1]) - 1])
        np.savetxt(open(filename, "wb"), output, fmt="%s")
        print(filename)

main()
