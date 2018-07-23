import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, cross_validation
from math import floor
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn import metrics
import pandas as pd
from ggplot import *
import scikitplot as skplt
import matplotlib.pyplot as plt
import re
import seaborn as sb

def ranking(pred_probs,test_count,top_k):
    to_rank=np.vstack([pred_probs,test_count]).T
    to_rank=to_rank[to_rank[:,0].argsort()[::-1]]
    test_count=np.sort(test_count)[::-1]
    print(np.sum([i in to_rank[:top_k,1] for i in test_count[:top_k]]))
    print(to_rank[:top_k,1])
    print(test_count[:top_k])
    return np.sum([i in to_rank[:top_k,1] for i in test_count[:top_k]])

def imp_graphlets(importants):
    names=['Ind_set', 'Only_edge', 'Wedge', 'Triangle','Ind.set', 'Only.edge', 'Matching', 'Only.wedge', 'Only.triangle', '3-star', '3-path', 'Tailed.triangle',
    '4-cycle', 'Diamond', '4-clique', 'Ind-set', 'Only-edge', 'Matching', 'Only-wedge', 'Only-triangle', 'Only-3-star', 'Only-3-path', 'Only-Tailed-tri', 'Only-4-cycle', 'Only-Diamond',
    'Only-4-clique', 'Wedge+edge', 'Triangle+edge', '4-star', 'Prong', '4-path', 'Forktailed-tri','Lontailed-tri','Doubletailed-tri','Tailed-4-cycle',
    '5-cycle','Hourglass','Cobra','Stingray','Hatted-4-cycle','3-wedge-col','3-tri-collision','Tailed-4-clique','Triangle-strip','Diamond-wed-col','4-wheel','Hatted-4-clique','Almost-5-clique','5-clique']
    indices=np.argsort(importants)
    return [names[i] for i in indices]

def aucDiff(tests,k):
    ids=np.append(k,"dist")
    tograph=pd.DataFrame(columns=ids)
    for i in range(len(tests)):
            a=np.loadtxt("karate_"+str(tests[i])+"/rocGraphs/"+str(tests[i])+"rocDist.txt")
            tograph.loc[i] = a.T
    tograph=pd.melt(tograph,id_vars=["dist"],var_name="k")
    tograph=tograph#[:12]
    print(tograph)
    plt.clf()
    bx=sb.pointplot(x=tograph['k'],y=tograph['value'],hue=tograph['dist'],legend=False)
    bx.set(xlabel='k', ylabel='Graphlet AUC - Degree AUC')
    leg_handles = bx.get_legend_handles_labels()[0]
    bx.legend(leg_handles, ['Mu=0.2,Dev=0.3', 'Mu=0.6,Dev=0.1','Mu=0.4,Dev=0.1'], title='Mu,STD')
    plt.savefig("karateDiff.png")
    return tograph


def lin_reg(x,y,counts,name,type,k):
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
       y_train, y_test = TE[:int(.7*len(local_g)),], TE[int(.7*len(local_g)):,]
       count_train, count_test=counts[:int(.7*len(local_g)),], counts[int(.7*len(local_g)):,]
       print(count_test)

       if (np.sum(y_train)) in [len(y_train),0] or (np.sum(y_test)) in [len(y_test),0]:
           return(np.sum(y_train))
       else:
           rfe = RFE(logreg, 1)
           rfe = rfe.fit(X_train, y_train)
           print(imp_graphlets(rfe.ranking_)[:5])
           logreg.fit(X_train, y_train)
           g_ranking=(np.argsort(-np.std(X_test, 0)*logreg.coef_)[:3][0][:5])
           #print("5 Most Important Graphlets: "+str(g_ranking))
           preds = logreg.predict_proba(X_test)
           ranking(preds[:,1],count_test,10)
           rocs=rocs+roc_auc_score(y_test,preds[:,1])
           print(roc_auc_score(y_test,preds[:,1]))
           skplt.metrics.plot_roc(y_test, preds, title=str(type)+", K="+str(k),classes_to_plot=[],plot_macro=True)
           plt.savefig(str(name)+'.png')
           skplt.metrics.plot_precision_recall(y_test, preds,classes_to_plot=[])
           plt.savefig(str(name)+'precrec.png')

    skplt.metrics.plot_confusion_matrix(y_test, logreg.predict(X_test), normalize=True)
    plt.savefig(str(name)+'conf.png')
    return rocs/5

data="socReed-63"
#test=[350,375,400,410,420]
test=[8,16,24,32,40] 
rocDiff=[0]*(len(test)+1)
for i in range(0,5):
    print("Graphlet Subgraph, k="+str(test[i]))
    a=lin_reg(str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(i)+".txt",str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(i)+".txt",str(data)+"/subGraphs_logistic/"+str(data)+"_count"+str(i)+".txt","./"+str(data)+"/rocGraphs/"+str(test[i])+str(data),"Graphlets",test[i])

    print("Degree Subgraph, k="+str(test[i]))
    b=lin_reg(str(data)+"/cent/"+str(data)+"_Xwave"+str(i)+".txt",str(data)+"/cent/"+str(data)+"_Ywave"+str(i)+".txt",str(data)+"/cent/"+str(data)+"_count"+str(i)+".txt","./"+str(data)+"/centROC/"+str(test[i])+str(data),"Degree",test[i])
    rocDiff[i]=a-b
    print("DIFF: "+str(a-b))
ending=(re.search(r'(?<=-)\w+', data))
if ending.group(0)=="uni":
    rocDiff[len(test)]=100
else:
    rocDiff[len(test)]=ending.group(0)
rocDiff=list(map(float,rocDiff))
np.savetxt(str(data)+"/rocGraphs/"+str(ending.group(0))+"rocDist.txt",rocDiff)
#aucDiff([23,63,"uni"],test)
#aucDiff([23,61,41],test)
