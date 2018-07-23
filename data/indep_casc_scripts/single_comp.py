import os, sys
import numpy as np
import networkx as nx
import random
sys.path.insert(0, '../../')
import models.indep_cascade as ic
import re
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

def deg(data,filename):
    tests=[8,16,24,32,40]
    logXdata = [[],[],[],[],[]]
    logYdata = [[],[],[],[],[]]
    logCountdata=[[],[],[],[],[]]
    gDat = open("../orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    G=nx.read_edgelist(gDat)
    E = np.loadtxt(open(os.path.join("../orig_graphs", filename), "rb"), dtype="int")
    w=np.loadtxt(os.path.join("../"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    weight=w[:,2]
    # make edge/weight matrix
    e=np.loadtxt(open(os.path.join("../"+"orig_graphs", filename), "rb"), dtype="int")[1:,:]
    ew=np.delete(np.hstack([e,w]),[2,3],1)
    for i in range(0,100):
        edge_file=("../"+str(data)+"/graphs/"+str(filename))
        if filename.endswith(".txt"):
            print(filename)

            node = random.randint(0, E[0,0]-1)
            indepcasc,active_list,times = ic.indep_casc(ew, node,90)

            i=0
            #find weighted degree for each node
            for edge in G.edges:
                G[edge[0]][edge[1]]['weight']=1
                # if edge[0] not in active_list or edge[1] not in active_list:
                #     G[edge[0]][edge[1]]['weight']=weight[i]
                # else:
                #     G[edge[0]][edge[1]]['weight']=0
                i+=1
            weighted_deg=np.array(G.degree(weight='weight'))
            deg=np.array(G.degree())
            deg_weights=np.hstack([deg,weighted_deg]).astype(float)
            deg_weights=np.delete(deg_weights,2,1)

            for node in active_list:
                #count number edges where a node is in subgraph and so is its neighbor
                toRemove=ew[(ew[:,0]==node)*(ew[:,1] in (active_list)),:].shape[0]
                deg_weights[deg_weights[:,0]==node,2]-=toRemove
            for k in range(0,len(tests)):
                if indepcasc >= tests[k]:
                    time_var=times[tests[k]-1]

                    active_nodes=active_list[:tests[k]]
                    actives=[0]*2
                    for nodes in active_nodes:
                        actives=[sum(x) for x in zip(actives,deg_weights[deg_weights[:,0]==int(nodes),:])]

                    actives=np.append(actives,time_var)
                    #appending cycles left when k nodes are infected
                    logXdata[k].append(actives)

                    #   deg_weights=np.delete(deg_weights,len(deg_weights)-1)
                    logCountdata[k].append(indepcasc)
                    if indepcasc >= 2*tests[k]:
                        logYdata[k].append(1)
                    else:
                        logYdata[k].append(0)
    for k in range(0,len(tests)):
        np.savetxt("../"+str(data)+"/cent/"+str(data)+"_Xwave"+str(k)+".txt",logXdata[k],fmt='%s')
        np.savetxt("../"+str(data)+"/cent/"+str(data)+"_Ywave"+str(k)+".txt",logYdata[k],fmt='%s')
        np.savetxt("../"+str(data)+"/cent/"+str(data)+"_count"+str(k)+".txt",logCountdata[k],fmt='%d')
    return 2

#takes string name of dataset and list of k's we want to test
#creates barplot breakdown of positive/negative doublings by k
def graph_dist(data,tests):
    tograph=pd.DataFrame(columns=['k','neg','pos'])
    i=0
    for filename in os.listdir("../"+str(data)+"/cent"):
        if re.match(r'.*_Ywave.*\.txt',filename):
            dat=np.loadtxt("../"+str(data)+"/cent/"+filename)
            df2=pd.DataFrame([[tests[i],len(dat)-np.count_nonzero(dat),np.count_nonzero(dat)]],columns=['k','neg','pos'])
            tograph=tograph.append(df2)
            i+=1
    tograph=pd.melt(tograph,id_vars=["k"],var_name="sign")
    print(tograph)
    plt.clf()
    bx=sb.barplot(x=tograph['k'],y=tograph['value'],hue=tograph['sign'])
    plt.savefig("../"+str(data)+"/cent/breakdown.png")
    return(2)

deg("socReed-63","socfb-Reed98.txt")
graph_dist("socReed-63",[8,16,24,32,40])
