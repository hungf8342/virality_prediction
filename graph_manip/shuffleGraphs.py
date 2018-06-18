import random
import networkx as nx

def shuffle(G, num):
    A = G
    i = 0
    while i < num:
        edgeList = [e for e in A.edges]
        indices = random.sample(xrange(len(edgeList)), 2)
        firstE = edgeList[indices[0]]
        secondE = edgeList[indices[1]]
        
        # need to avoid situation like, [(1,2), (1,3), (2,4)] -> [(1,3), (1,4), (2,,2)]
        if (firstE[1] != secondE[0]) and \
           (firstE[0] != secondE[1]) and \ 
           (not A.has_edge(firstE[0], secondE[1])) and \
           (not A.has_edge(secondE[0], firstE[1])):
            A.remove_edge(firstE[0], firstE[1])
            A.remove_edge(secondE[0], secondE[1])
            A.add_edge(firstE[0], secondE[1])
            A.add_edge(secondE[0], firstE[1])
            i += 1
    return A
