import numpy as np
import random
import networkx as nx
import os, sys
sys.path.insert(0, '../')
import models.hawkes as hs
import graph_manip.graphAttribs as ga
import pickle

# Loads the local graphlet vector for each node
def loadMap(filename, numNodes):
    
    # Initialize a vector for each node
    nodeCount = np.zeros((numNodes, 46))

    # Open the edge-to-graphlet file
    graphlets = open(os.path.join("graphlets", filename), "rb")
    
    # Iterate through every edge
    for line in graphlets:

        # Add the graphlet count for an edge to its 
        # corresponding nodes
        data = line.split()
        n1 = int(data[0])
        n2 = int(data[1][:-1])
        for i in range(46):
            nodeCount[n1][i] += int(data[i + 2])
            nodeCount[n2][i] += int(data[i + 2])
    return nodeCount

# Loads the secondary degree of each node
def loadSecondDeg(G, theta):
    degrees = np.zeros(len(G.nodes()))
    deg_map = G.degree()
    for i in range(len(degrees)):
        degrees[i] = theta * deg_map[i]
        for edge in G.edges(i):
            degrees[i] += (theta ** 2) * deg_map[edge[1]]
            for edge2 in G.edges(edge[1]):
                degrees[i] += (theta ** 3) * deg_map[edge2[1]]
                for edge3 in G.edges(edge2[1]):
                    degrees[i] += (theta ** 4) * deg_map[edge3[1]]
    
    return degrees

def main():
    lgCount = []
    egCount = []
    ggCount= []
    sec_degs = []
    cl_centData = []
    dg_centData = []
    ev_centData = []
    l_hawkes = []
    g_hawkes = []
    count = 0
    first = True
    total_theta = 0
    total_num = 0
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"): 
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            total_theta += ga.getCritTheta(G)
            total_num += 1
            print(str(total_num) + ': \t' + str((1.0 * total_theta)/total_num))
            sys.stdout.flush()

    
    theta = np.real(total_theta) / total_num
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])
    
            # Load up the local graphlet counts
            nodeCount = loadMap(filename, N)
            
            sec_deg = loadSecondDeg(G, theta * 0.93)
            # Load up GUISE global graphlet counts
#            globalDat = np.loadtxt(os.path.join("global_graphlets",
#                                    filename), dtype=int,
#                                    usecols=[1]) 

            # Load up the e-clog global graphlet counts
            totalGraphlets = np.sum(nodeCount, axis=0) 

            # Calculate the expected hawkes events from each
            # node
            hVec = hs.getHawkesVec(G, theta * 0.93)

#            cent = nx.closeness_centrality(G)
#            deg_c = nx.degree_centrality(G)
#            eig_c = nx.eigenvector_centrality(G)
            
            if len(hVec) > 0:
                for i in range(N):
                    #i = random.randint(0, N - 1)
#                    centrality = cent[i]
                    hawkes = hVec[i]
                    lgCount.append(nodeCount[i])
#                    ggCount.append(globalDat)
                    l_hawkes.append(hawkes)
                    g_hawkes.append(np.mean(hVec))
                    sec_degs.append(sec_deg[i])
#                    cl_centData.append(centrality)
#                    dg_centData.append(deg_c[i])
#                    ev_centData.append(eig_c[i])
                    
                    egCount.append(totalGraphlets)
                    count += 1
                print(count)
                sys.stdout.flush()
            else:
                print("-1")
    pickle.dump((lgCount, egCount, ggCount, sec_degs, l_hawkes, g_hawkes, cl_centData, dg_centData, ev_centData), open("outDataLocal_second_deg.dat", 'wb'))
main()
