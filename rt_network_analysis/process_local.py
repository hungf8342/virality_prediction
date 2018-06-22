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
    yData = []
    count = 0
    first = True
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            E = np.loadtxt(open(os.path.join("graphs", filename[:-4] + ".dat"), "rb"), dtype="int")
            nodeCount = loadMap(filename, E[0,0])
            if first:
                theta = ga.getCritTheta(E[1:])
                first = False
            D = hs.getDiag(E[1:], theta * 0.96)
            if len(D) > 0:
                print(filename)
                print(count)
                for i in range(E[0,0]):
                    #i = random.randint(0, E[0,0] - 1)
                    hawkes = hs.exact_hawkes_from_diag(D, i)
                    if hawkes > 0:
                        xData.append(nodeCount[i])
                        yData.append(hawkes)
                    count += 1
            else:
                print("-1")
    pickle.dump((xData, yData), open("outDataLocal_rt-pol.dat", 'wb'))
main()
