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
    xData = []
    ggCount = []
#    centData = []
    yData = []
    count = 0
    first = True
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])

            nodeCount = loadMap(filename, N)
            totalGraphlets = np.sum(nodeCount, axis=0)
            if first:
                theta = ga.getCritTheta(G)
                first = False
            hVec = hs.getHawkesVec(G, theta * 0.96)
#            cent = nx.closeness_centrality(G)
            if len(hVec) > 0:
                #for i in range(N):
                i = random.randint(0, N - 1)
#                centrality = cent[i]
                hawkes = hVec[i]
                xData.append(nodeCount[i])
                yData.append(hawkes)
#                centData.append(centrality)
                ggCount.append(totalGraphlets)
                print(count)
                count += 1
            else:
                print("-1")
    pickle.dump((xData, yData, ggCount), open("outDataLocal_rt-pol.dat", 'wb'))
main()
