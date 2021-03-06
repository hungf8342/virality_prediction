import networkx as nx
import subprocess
import numpy as np
import csv
import os, sys
import random
sys.path.insert(0, '../')
import models.indep_cascade as ic
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import re


#for each node, calculate LIR score: the lower the score, the bigger degree that node has relative to neighbors
def lir(graph):
    lirs=[0]*(len(graph.nodes())+1)
    for node in graph.nodes():
        neighbors=list(graph[str(int(node))].keys())
        degs=dict(graph.degree(neighbors))
        lirs[(int(node))]=sum(graph.degree(node)<deg for deg in list(degs.values()))
    return lirs

#takes networkx network and list of k active nodes
#returns subgraph of up to 2-level neighbors connected to the k nodes
def find_neighbors(graph,active_list):
    subGraph=nx.Graph()
    nodes=set()
    #appending neighbors
    for node in active_list:
        neighbors=list(graph[str(int(node))].keys())
        nodes.update(neighbors)
    neighsq=set()
    #appending neighbors of neighbors
    for node in nodes:
        neighbors=list(graph[str(int(node))].keys())
        neighsq.update(neighbors)
    #removing k node to k node edges, returning subgraph
    sub=graph.subgraph(list(nodes.union(neighsq))).copy()
    active_list=list(map(int,active_list))
    active_list=list(map(str,active_list))
    h=graph.subgraph(active_list).copy()
    sub.remove_edges_from(h.edges)
    return sub

def setup(data,filename):
    gDat = open("../data/orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    graph=nx.read_edgelist(gDat)
    lir_scores=lir(graph)
    E = np.loadtxt(open(os.path.join("../data/orig_graphs", filename), "rb"), dtype="int")
    weight=np.loadtxt(os.path.join("../data/"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    return graph,lir_scores,E,weight


def deg_setup(numNodes,graph,E,weight):
    #run indep casc simulation
    i = random.randint(0, E[0,0] - 1)
    indepcasc,active_list,times = ic.indep_casc(weight, [i], 500)
    print(indepcasc)
    numNodes.append(indepcasc)
    #find degrees of all nodes
    deg=np.array(graph.degree())
    active_list=list(map(float,active_list))
    deg=deg.astype(int)
    return indepcasc,active_list,deg

def guise(subgraph,data,filename):
    nx.write_edgelist(subgraph,os.path.join("../data/"+str(data)+"/subgraphs",filename),data=False)
    sanitize="python ../escape/python/sanitize.py "+"../data/"+str(data)+"/subgraphs "+ str(filename)+" >log.txt"
    os.system(sanitize)
    os.remove(os.path.join("../data/"+str(data)+"/subgraphs",filename))
    cmd="python ../escape/wrappers/subgraph_counts.py "+"../data/"+str(data)+"/subgraphs/"+filename[:-4]+".edges"+" 5"+" >log.txt"
    os.system(cmd)
    line=np.loadtxt("out.txt")[2:]
    return line

def main_subgraph(data,filename,X):
        count = 0
        tests=[5,10,15,20,25]
        logdegdata = [[],[],[],[],[]]
        loggraphdata = [[],[],[],[],[]]
        logYdata = [[],[],[],[],[]]
        logCountdata=[[],[],[],[],[]]
        numNodes=[]
        graph,lir_scores,E,weight=setup(data,filename)

        for i in range(0,100):
            print(filename)
            print(i)
            #load edges, weight, choose a random starting node to run IC from for 20 iterations
            if filename.endswith("txt"):
                indepcasc,active_list,deg=deg_setup(numNodes,graph,E,weight)
                for node in active_list:
                #count number edges where a node is in subgraph and so is its neighbor
                    neighbor_in=np.isin(E[:,1],active_list)
                    node_in=np.isin(E[:,0],active_list)
                    toRemove=E[(E[:,0]==node)*neighbor_in,:].shape[0]+E[(E[:,1]==node)*node_in,:].shape[0]
                    deg[deg[:,0]==node,1]-=toRemove
                #for each k value to be tested, determine whether the cascade size is larger than k
                #add such cascade starting node profiles and whether they're larger than 2k to different txt files
                for k in range(0,len(tests)):
                    if indepcasc >= tests[k]:
                        active_nodes=active_list[:tests[k]]
                        subgraph=find_neighbors(graph,active_nodes)
                        actives=guise(subgraph,data,filename)
                        actives_deg=[0]*2
                        for nodes in active_nodes:
                            actives_deg=[sum(x) for x in zip(actives_deg,deg[deg[:,0]==int(nodes),1])]
                        #for the kth value of initial cascade sizes to be tested,
                        #add the new degree and graphlet features to the right list
                        logdegdata[k].append(actives_deg)
                        loggraphdata[k].append(actives)
                        logCountdata[k].append(indepcasc)
                        if indepcasc >= X*tests[k]:
                            logYdata[k].append(1)
                        else:
                            logYdata[k].append(0)
                        count+=1
        np.savetxt("../data/"+str(data)+"/"+str(data)+"_counts"+".txt",numNodes,fmt='%d')

        #save cascade sizes, subgraph graphlet features, and doubling for each subgraph for each k.
        for k in range(0,len(tests)):
            logdegdata[k]=np.vstack(logdegdata[k])
            loggraphdata[k]=np.vstack(loggraphdata[k])
            np.savetxt("../data/"+str(data)+"/cent/"+str(data)+"_Xwave"+str(k)+".txt",logdegdata[k],fmt='%s')
            np.savetxt("../data/"+str(data)+"/cent/"+str(data)+"_Ywave"+str(k)+".txt",logYdata[k],fmt='%s')
            np.savetxt("../data/"+str(data)+"/cent/"+str(data)+"_count"+str(k)+".txt",logCountdata[k],fmt='%d')
            np.savetxt("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_count"+str(k)+".txt",logCountdata[k],fmt='%d')
            np.savetxt("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(k)+".txt",loggraphdata[k],fmt='%d')
            np.savetxt("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(k)+".txt",logYdata[k],fmt='%d')

#takes string name of dataset and list of k's we want to test
#creates barplot breakdown of positive/negative doublings by k
def graph_dist(data,tests):
    tograph=pd.DataFrame(columns=['k','neg','pos'])
    i=0
    for filename in os.listdir("../data/"+str(data)+"/subGraphs_logistic"):
        if re.match(r'.*_Ywavesub.*\.txt',filename):
            dat=np.loadtxt("../data/"+str(data)+"/subGraphs_logistic/"+filename)
            df2=pd.DataFrame([[tests[i],len(dat)-np.count_nonzero(dat),np.count_nonzero(dat)]],columns=['k','neg','pos'])
            tograph=tograph.append(df2)
            i+=1
    tograph=pd.melt(tograph,id_vars=["k"],var_name="sign")
    print(tograph)
    plt.clf()
    bx=sb.barplot(x=tograph['k'],y=tograph['value'],hue=tograph['sign'])
    plt.savefig("../data/"+str(data)+"/breakdown.png")
    return(2)

#graph_dist("socReed-X10",[5,10,15,20,25])
