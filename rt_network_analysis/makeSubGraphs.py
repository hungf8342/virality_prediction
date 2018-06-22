import networkx as nx
import random
import Queue
import numpy as np

def makeSubGraph(graph, size, N):
    curSize = 0
    while curSize != size:
        node = random.randint(0, N - 1)
        toVisit = Queue.Queue()
        visited = set()

        toVisit.put(str(node))
        visited.add(str(node))
        curSize = 1
        while not toVisit.empty():
            curNode = toVisit.get()
            for edge in graph.edges([curNode]):
                if edge[1] not in visited:
                    if curSize < size:
                        toVisit.put(edge[1])
                        visited.add(edge[1])
                        curSize += 1
    return graph.subgraph(visited)
    
def genSubGraphs(filename, dest, size, num): 
    f = open(filename, "rb")
    firstLine = f.readline().split()
    N = int(firstLine[0])
    G = nx.read_edgelist(f)

    for i in range(num):
        print("Graph:" +  str(i))
        tempG = makeSubGraph(G, size, N)
        nodes = tempG.nodes()
        nToInd = dict(zip(nodes, range(len(nodes))))
        output = [[str(size), str(tempG.number_of_edges())]]
        for line in nx.generate_edgelist(tempG):
            vals = line.split()
            output.append([nToInd[vals[0]],nToInd[vals[1]]])
        np.savetxt(open(dest + str(i) + ".dat", "wb"), output, fmt="%s")

genSubGraphs("orig_graph/rt-pol.txt", "graphs/rt-pol_", 500, 100)
