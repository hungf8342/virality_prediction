import numpy as np
import random
import networkx as nx
import os, sys
sys.path.insert(0, '../')
import models.hawkes as hs
import graph_manip.graphAttribs as ga
import pickle

def loadMap(filename, numNodes):
    nodeCount = np.zeros((numNodes, 46))
    graphlets = open(os.path.join("graphlets", filename), "rb")
    for line in graphlets:
        data = line.split()
        n1 = int(data[0])
        n2 = int(data[1][:-1])
        for i in range(46):
            nodeCount[n1][i] += int(data[i + 2])
            nodeCount[n2][i] += int(data[i + 2])
    return nodeCount
def main():
    lgCount = []
    egCount = []
    ggCount= []
    cl_centData = []
    dg_centData = []
    ev_centData = []
    l_hawkes = []
    g_hawkes = []
    count = 0
    first = True
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])
    
            # Load up the local graphlet counts
            nodeCount = loadMap(filename, N)

            # Load up GUISE global graphlet counts
            globalDat = np.loadtxt(os.path.join("global_graphlets",
                                    filename), dtype=int,
                                    usecols=[1]) 

            # Load up the e-clog global graphlet counts
            totalGraphlets = np.sum(nodeCount, axis=0)
            
            # Calculate the appropriate theta for this run
            # based on the first shuffled graph
            if first:
                theta = ga.getCritTheta(G)
                first = False

            # Calculate the expected hawkes events from each
            # node
            hVec = hs.getHawkesVec(G, theta * 0.96)

            cent = nx.closeness_centrality(G)
            deg_c = nx.degree_centrality(G)
            eig_c = nx.eigenvector_centrality(G)
            
            if len(hVec) > 0:
                for i in range(N):
                    #i = random.randint(0, N - 1)
                    centrality = cent[i]
                    hawkes = hVec[i]
                    lgCount.append(nodeCount[i])
                    ggCount.append(globalDat)
                    l_hawkes.append(hawkes)
                    g_hawkes.append(np.mean(hVec))
                    
                    cl_centData.append(centrality)
                    dg_centData.append(deg_c[i])
                    ev_centData.append(eig_c[i])
                    
                    egCount.append(totalGraphlets)
                    print(count)
                    count += 1
            else:
                print("-1")
    pickle.dump((lgCount, egCount, ggCount, l_hawkes, g_hawkes, cl_centData, dg_centData, ev_centData), open("outDataLocal_rt-pol.dat", 'wb'))
main()
