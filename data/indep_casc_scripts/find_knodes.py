import sys,os
sys.path.insert(0, '../../')
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

def lir_find(data,filename):
    weight=np.loadtxt(os.path.join("../"+str(data)+"/weight",str(data)+"_s_0" + ".txt"))
    gDat = open("../orig_graphs/"+filename, 'rb')
    firstLine = gDat.readline().split()
    graph=nx.read_edgelist(gDat)
    print(len(list(range(0,len(graph.nodes())+1))))
    print(len(lir(graph)))
    #sort nodes by lir score: retain 0-LIR score Nodes
    d={'nodes':list(range(0,len(graph.nodes())+1)),'lir':lir(graph)}
    lir_index=pd.DataFrame(data=d)
    print(lir_index)
    zero_lir=lir_index.loc[(lir_index['lir']==0)]
    logreg=cPickle.load(open("regmodel.sav",'rb'))
    print(list(zero_lir.index))
    count_f,act,tim=ic.indep_casc(weight,[256,889,1446],1000)
    print(count_f)
    #count,actives,time=ic.indep_casc(weight,list(zero_lir.index),1000)
    #print(count)
    # run a single-casc simul from each, get their probability of doubling or x-factoring
    for node in list(zero_lir.index):
        count,actives,time=ic.indep_casc(weight,[node],5)
        #find graphlet _countssubgraph=find_neighbors(graph,active_nodes)
        subgraph=find_neighbors(graph,actives)
        nx.write_edgelist(subgraph,os.path.join("../"+str(data)+"/subgraphs",filename),data=False)
        sanitize="python ../../escape/python/sanitize.py "+"../"+str(data)+"/subgraphs "+ str(filename)+" >log.txt"
        os.system(sanitize)
        os.remove(os.path.join("../"+str(data)+"/subgraphs",filename))
        cmd="python ../../escape/wrappers/subgraph_counts.py "+"../"+str(data)+"/subgraphs/"+filename[:-4]+".edges"+" 5"+" >log.txt"
        os.system(cmd)
        line=np.loadtxt("out.txt")[2:]
        actives=line
        actives=np.append(actives,1)
        actives=actives.reshape(1,-1)


        print(logreg.predict_proba(actives))

    #pick the top k nodes, test
    return count
data="socReed-X10"
lin_reg("../"+str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub.txt","../"+str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub.txt","../"+str(data)+"/subGraphs_logistic/"+str(data)+"_count.txt")
lir_find("Haverford-31","soc-Haverford.txt")
