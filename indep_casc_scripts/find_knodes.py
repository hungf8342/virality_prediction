import sys,os
sys.path.insert(0, '../')
import models.indep_cascade as ic
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

#takes networkx network and list of k active nodes
#returns subgraph of up to 2-level neighbors connected to the k nodes
def find_neighbors(graph,active_list):
    subGraph=nx.Graph()
    nodes=set()
    #appending neighbors
    for node in active_list:
        #print(node)
        neighbors=list(graph[str(int(node))].keys())
        nodes.update(neighbors)
    neighsq=set()
    #appending neighbors of neighbors
    for node in nodes:
        neighbors=list(graph[str(int(node))].keys())
        neighsq.update(neighbors)

    sub=graph.subgraph(list(nodes.union(neighsq))).copy()
    active_list=list(map(int,active_list))
    active_list=list(map(str,active_list))
    h=graph.subgraph(active_list).copy()
    sub.remove_edges_from(h.edges)
    return sub
#for each node, calculate LIR score: the lower the score, the bigger degree that node has relative to neighbors
def lir(graph):
    lirs=[0]*(len(graph.nodes())+1)
    for node in graph.nodes():
        neighbors=list(graph[str(int(node))].keys())
        degs=dict(graph.degree(neighbors))
        #print(lirs[int(node)])
        lirs[(int(node))]=sum(graph.degree(node)<deg for deg in list(degs.values()))
    #print(lirs)
    return lirs
def lin_reg(x,y,counts):
    local_g=np.loadtxt(x)
    TE=np.loadtxt(y)
    counts=np.loadtxt(counts)

    #print(local_g.shape)
    local_train, local_test, TE_train, TE_test = train_test_split(local_g, TE, test_size=0.7, random_state=0)


    logreg=linear_model.LogisticRegression()
    rocs=0
    kf = cross_validation.KFold(len(y), n_folds=5)
    i=0
    for train_index, test_index in kf:

       X_train, X_test = local_g[:int(.7*len(local_g))], local_g[int(.7*len(local_g)):]
       if local_g.ndim==1:
           X_train,X_test=np.reshape(X_train,(-1,1)),np.reshape(X_test,(-1,1))
       y_train, y_test = TE[:int(.7*len(local_g)),], TE[int(.7*len(local_g)):,]
       count_train, count_test=counts[:int(.7*len(local_g)),], counts[int(.7*len(local_g)):,]

       if (np.sum(y_train)) in [len(y_train),0] or (np.sum(y_test)) in [len(y_test),0]:
           return(np.sum(y_train))
       else:
           logreg.fit(X_train, y_train)
           cPickle.dump(logreg,open("regmodel.sav",'wb'))
           preds = logreg.predict_proba(X_test)

           #calculating ROCs, saving AUC plot
           rocs=rocs+roc_auc_score(y_test,preds[:,1])
    return rocs/5

def eig_cent(data,filename):
    weight=np.loadtxt(os.path.join("../data/"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    gDat = open("../data/orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    graph=nx.read_edgelist(gDat)
    eig=pd.DataFrame.from_dict(nx.eigenvector_centrality(graph),orient='index')
    eig['nodes'] = eig.index

    sorte=eig.sort_values(by=0,axis=0,ascending=False)
    nodes=sorte.iloc[:3,1].values.tolist()
    print(nodes)
    count_f,act,tim=ic.indep_casc(weight,nodes,1000)
    print(count_f)


def lir_find(data,filename):
    weight=np.loadtxt(os.path.join("../data/"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    gDat = open("../data/orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    graph=nx.read_edgelist(gDat)
    #print(len(list(range(0,len(graph.nodes())+1))))
    #print(len(lir(graph)))
    #sort nodes by lir score: retain 0-LIR score Nodes
    d={'nodes':list(range(0,len(graph.nodes())+1)),'lir':lir(graph)}
    lir_index=pd.DataFrame(data=d)
    #print(lir_index)
    zero_lir=lir_index.loc[np.isin(lir_index['lir'],[0])]
    logreg=cPickle.load(open("regmodel.sav",'rb'))
    #print(list(zero_lir.index))

    top_k=[]

    #count,actives,time=ic.indep_casc(weight,list(zero_lir.index),1000)
    #print(count)
    # run a single-casc simul from each, get their probability of doubling or x-factoring
    for node in list(zero_lir.index):
        print(node)
        print("degree: " +str(graph.degree(str(node))))
        count,actives,time=ic.indep_casc(weight,[node],5)
        #print(graph.degree(str(node)))
        #find graphlet _countssubgraph=find_neighbors(graph,active_nodes)
        if (type(graph.degree(str(node)))==int):
            subgraph=find_neighbors(graph,actives)
            nx.write_edgelist(subgraph,os.path.join("../data/"+str(data)+"/subgraphs",filename),data=False)
            sanitize="python ../escape/python/sanitize.py "+"../data/"+str(data)+"/subgraphs "+ str(filename)+" >log.txt"
            os.system(sanitize)
            os.remove(os.path.join("../data/"+str(data)+"/subgraphs",filename))
            cmd="python ../escape/wrappers/subgraph_counts.py "+"../data/"+str(data)+"/subgraphs/"+filename[:-4]+".edges"+" 5"+" >log.txt"
            os.system(cmd)
            line=np.loadtxt("out.txt")[2:]
            actives=line
            #actives=np.append(actives,1)
            actives=actives.reshape(1,-1)


            #print(logreg.predict_proba(actives)[0][1])
            top_k.append([node,logreg.predict_proba(actives)[0][1]])
        #print(count)
    top_k=np.vstack(top_k)

    nodes=top_k[top_k[:,1].argsort()][::-1][:3,0]
    print(nodes)
    count_f,act,tim=ic.indep_casc(weight,nodes,1000)
    print(count_f)
    #pick the top k nodes, test

    return count
data="alv-X10"
lin_reg("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub4.txt","../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub4.txt","../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_count4.txt")
lir_find("alv-X10","soc-advogato.txt")
eig_cent(data,"soc-advogato.txt")
