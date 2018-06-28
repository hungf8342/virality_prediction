import numpy as np
import random
import networkx as nx
import os, sys
import matplotlib.pyplot as plt
sys.path.insert(0, '../')
import models.indep_cascade as ic

def loadMap(filename, numNodes,data):
    nodeCount = np.zeros((numNodes, 47))
    graphlets = open(os.path.join(str(data)+"/graphlets", filename), "rb")
    weight=np.loadtxt(os.path.join(str(data)+"/weight",filename[:-4] + ".dat"))
    for i in range(int(numNodes)):
        nodeCount[i][46]=(np.sum(weight[weight[:,0]==i,2])+np.sum(weight[weight[:,1]==i,2]))
    for line in graphlets:
        data = line.split()
        n1 = int(data[0])
        n2 = int(data[1][:-1])
        for i in range(46):
            nodeCount[n1][i] += int(data[i + 2])
            nodeCount[n2][i] += int(data[i + 2])
    return nodeCount

#given k nodes, find nodecount[k] and avoid adding duplicate edge graphlet counts. we can
#in fact remove all edges between the nodes.
def loadMap2(filename,nodeCount_loaded,activeNodes,data):
    nodeCount = nodeCount_loaded
    graphlets = open(os.path.join(str(data)+"/graphlets", filename), "rb")
    weight=np.loadtxt(os.path.join(str(data)+"/weight",filename[:-4] + ".dat"))
    #print("active Nodes: "+str(activeNodes))
    for line in graphlets:
        data = line.split()
        n1 = int(data[0])
        n2 = int(data[1][:-1])
        if n2 in activeNodes and n1 in activeNodes:
            #print(str(n1)+str(n2)+": "+str(n2 in activeNodes and n1 in activeNodes))
            for i in range(46):
                nodeCount[n1][i] -= int(data[i + 2])
                nodeCount[n2][i] -= int(data[i + 2])
    for line in weight:
        line=' '.join(map(str, line))
        data=line.split()
        n1 = int(float(data[0]))
        n2 = int(float(data[1][:-1]))
        if n2 in activeNodes and n1 in activeNodes:
            print(str(n1)+str(n2)+": "+str(n2 in activeNodes and n1 in activeNodes))
            nodeCount[n1][46] -= int(float(data[2]))
            nodeCount[n2][46] -= int(float(data[2]))
    return nodeCount

#main function for predicting logistically based on a starting node whether a cascade of
#size k will grow to size 2k.
def main1(data):
    count = 0
    tests=[2,3,5,7,8]
    logXdata = [[],[],[],[],[]]
    logYdata = [[],[],[],[],[]]
    for filename in os.listdir(str(data)+"/graphlets"):
        if filename.endswith("gfc"):
            E = np.loadtxt(open(os.path.join(str(data)+"/graphs", filename[:-4] + ".dat"), "rb"), dtype="int")
            nodeCount = loadMap(filename, E[0,0],data)
            weight=np.loadtxt(os.path.join(str(data)+"/weight",filename[:-4] + ".dat"))
            i = random.randint(0, E[0,0] - 1)
            indepcasc,active_list = ic.indep_casc(weight, i,20)
            #for each k value to be tested, determine whether the cascade size is larger than k
            #add such cascade starting node profiles and whether they're larger than 2k to different txt files
            for k in range(0,len(tests)):
                if indepcasc >= tests[k]:
                    print(count)
                    logXdata[k].append(nodeCount[i])
                    if indepcasc >= 2*tests[k]:
                        logYdata[k].append(1)
                    else:
                        logYdata[k].append(0)
                    count+=1
    for k in range(0,len(tests)):
        np.savetxt(str(data)+"/singleNode_logistic/"+str(data)+"_Xwave"+str(k)+".txt",logXdata[k],fmt='%d')
        np.savetxt(str(data)+"/singleNode_logistic/"+str(data)+"_Ywave"+str(k)+".txt",logYdata[k],fmt='%d')

#main function for predicting logistically growth from a k-size cascade to 2k, given dolphin_graphlets
#of the k-subgraph. We exclude edges between nodes in the subgraph.
def main2(data):
        count = 0
        tests=[2,3,5,7,8]
        logXdata = [[],[],[],[],[]]
        logYdata = [[],[],[],[],[]]
        numNodes=[]
        for filename in os.listdir(str(data)+"/graphlets"):
            #load edges, weight, choose a random starting node to run IC from for 20 iterations
            if filename.endswith("gfc"):
                E = np.loadtxt(open(os.path.join(str(data)+"/graphs", filename[:-4] + ".dat"), "rb"), dtype="int")
                i = random.randint(0, E[0,0] - 1)
                weight=np.loadtxt(os.path.join(str(data)+"/weight",filename[:-4] + ".dat"))
                indepcasc,active_list = ic.indep_casc(weight, i,20)
                numNodes.append(indepcasc)
                nodeCount = loadMap(filename, E[0,0],data)

                #for each k value to be tested, determine whether the cascade size is larger than k
                #add such cascade starting node profiles and whether they're larger than 2k to different txt files
                for k in range(0,len(tests)):
                    nodeCount= loadMap2(filename,nodeCount,active_list[:k],data)
                    if indepcasc >= tests[k]:
                        print(count)
                        active_nodes=active_list[:tests[k]]
                        actives=[0]*46
                        for node in active_nodes:
                            actives=[sum(x) for x in zip(actives,nodeCount[int(node)])]
                        logXdata[k].append(actives)
                        print("sum of graphlets "+str(actives))
                        if indepcasc >= 2*tests[k]:
                            logYdata[k].append(1)
                        else:
                            logYdata[k].append(0)
                        count+=1
        np.savetxt(str(data)+"/"+str(data)+"_counts"+".txt",numNodes,fmt='%d')
        for k in range(0,len(tests)):
            np.savetxt(str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(k)+".txt",logXdata[k],fmt='%d')
            np.savetxt(str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(k)+".txt",logYdata[k],fmt='%d')



main1("socfb-Reed98")
main2("socfb-Reed98")
