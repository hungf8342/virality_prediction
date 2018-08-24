import sys,os
sys.path.insert(0, '../')
import models.indep_cascade as ic
import joint_single as ms
import neighbors_twolevel as nt
import pandas as pd
import networkx as nx
import numpy as np
from sklearn import datasets, linear_model, cross_validation
from math import floor
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import metrics
import _pickle as cPickle
from collections import Counter

#inputs: networkx network and list of k active nodes
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
    #remove original node-to-node edges
    sub=graph.subgraph(list(nodes.union(neighsq))).copy()
    active_list=list(map(int,active_list))
    active_list=list(map(str,active_list))
    h=graph.subgraph(active_list).copy()
    sub.remove_edges_from(h.edges)
    return sub

#inputs: train/test/count data as txt files
#output and saves a logistic model, returns
def log_reg(x,y,counts):
    local_g=np.loadtxt(x)
    TE=np.loadtxt(y)
    counts=np.loadtxt(counts)
    #divide training/test data and save resulting model
    logreg=linear_model.LogisticRegression()
    X_train, y_train,count_train,X_test,y_test,count_test = nt.train_test(local_g,TE,counts)

    if (np.sum(y_train)) in [len(y_train),0] or (np.sum(y_test)) in [len(y_test),0]:
        return(np.sum(y_train))
    else:
        logreg.fit(X_train, y_train)
        cPickle.dump(logreg,open("regmodel.sav",'wb'))
        preds = logreg.predict_proba(X_test)
    return preds

#inputs: network name data, original graph file, k
#returns nodes in sorted by eigenvector centrality, cascade size returned from using the k top nodes
def eig_cent(data,filename,k):
    graph,lir_scores,E,weight=ms.setup(data,filename)
    eig=pd.DataFrame.from_dict(nx.eigenvector_centrality(graph),orient='index')
    eig['nodes'] = eig.index

    sorte=eig.sort_values(by=0,axis=0,ascending=False)
    nodes=sorte.iloc[:k,1].values.tolist()
    count_f,act,tim=ic.indep_casc(weight,nodes,1000)
    print(count_f)
    return nodes,count_f


def lir_find(data,filename,k):
    graph,lir_scores,E,weight=ms.setup(data,filename)
    #sort nodes by lir score: retain 0-LIR score Nodes
    d={'nodes':list(range(0,len(graph.nodes())+1)),'lir':ms.lir(graph)}
    lir_index=pd.DataFrame(data=d)
    zero_lir=lir_index.loc[np.isin(lir_index['lir'],[0])]
    logreg=cPickle.load(open("regmodel.sav",'rb'))
    top_k=[]

    # run a single-casc simul from each, get their probability of x-factoring
    for node in list(zero_lir.index):
        print(node)
        count,active_nodes,time=ic.indep_casc(weight,[node],10)
        #find graphlet counts
        if (type(graph.degree(str(node)))==int):
            subgraph=find_neighbors(graph,active_nodes)
            actives=ms.guise(subgraph,data,filename)
            actives=actives.reshape(1,-1)
            #append node and predicted prob that size will multiply by factor X
            top_k.append([node,logreg.predict_proba(actives)[0][1]])
    top_k=np.vstack(top_k)

    nodes=top_k[top_k[:,1].argsort()][::-1][:k,0]
    count_f,act,tim=ic.indep_casc(weight,nodes,len(graph.nodes()))
    return nodes,count_f

#inputs: data name, original graph file, number of top nodes wanted
#takes a graphlet regression model and finds top k nodes, same using eigenvector centrality
def find_k(data,filename,k):
    log_reg("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub1.txt","../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub1.txt","../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_count1.txt")
    g_nodes,count_g=lir_find(data,filename,k)
    e_nodes,count_e=eig_cent(data,filename,k)
    return g_nodes,e_nodes,count_g,count_e

#inputs: data name, original graph file, number of top nodes wanted
#runs find_k 4 times and chooses the top k aggregated nodes as the final top k
def test_eff(data,filename,k):
    weight=np.loadtxt(os.path.join("../data/"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    gDat = open("../data/orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    graph=nx.read_edgelist(gDat)
    g_bin=list()
    e_bin=list()
    for i in range(4):
        g_nodes,e_nodes,count_g,count_e=find_k(data,filename,k)
        g_bin.append(g_nodes)
        e_bin.append(e_nodes)
    g_top=Counter([x for y in g_bin for x in y]).most_common(k)
    e_top=Counter([x for y in e_bin for x in y]).most_common(k)
    g_nodek=[x[0] for x in g_top]
    e_nodek=[x[0] for x in e_top]
    count_g,actives,time=ic.indep_casc(weight,g_nodek,len(graph.nodes())/5*k)
    count_e,actives,time=ic.indep_casc(weight,e_nodek,len(graph.nodes())/5*k)
    for save,val in zip(["count_g","node_g","count_e","node_e"],[count_g,g_nodek,count_e,e_nodek]):
        file="../data/"+str(data)+"/testing/"+str(k)+str(save)+".txt"
        with open(file,"a") as myfile:
             myfile.write(str(val)+'\n')
    print(count_g)
    print(count_e)

#test_eff("Caltech-X10","socfb-Caltech36.txt",0)
