import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, cross_validation
from math import floor
import pandas as pd
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split

def cascade_dist(x):
    cascade_size=np.loadtxt(x)
    cascade_size=cascade_size[cascade_size<16]
    plt.figure(figsize=(9, 6))
    plt.title("Cascade Size Counts (Karate)",size=16)
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(range(0, 16, 1),fontsize=10)
    plt.yticks(range(0, 3000, 200), fontsize=10)
    plt.xlabel("Cascade Size", fontsize=13)
    plt.ylabel("Count", fontsize=13)
    plt.hist(cascade_size,bins=20,color="#3F5D7D")
    plt.show()

def graphlet_sig(x,y):
    local_g=pd.DataFrame(np.loadtxt(x))
    TE=np.loadtxt(y)

    table=pd.crosstab(local_g[4,2,5],TE)
    print(table)
    table.hist(bins=20, stacked=True)
    plt.xlabel('expected IC events')
    plt.ylabel('Number of g4')
    plt.show()

def lin_reg(x,y):
    local_g=np.loadtxt(x)
    TE=np.loadtxt(y)
    #TE=np.log(np.asarray([TE]).T)
    #print(local_g.shape)
    #local_train, local_test, TE_train, TE_test = train_test_split(local_g, TE, test_size=0.7, random_state=0)


    # local_train=local_g[:800,]
    # local_test=local_g[800:]
    #
    # TE_train=(TE[:800,])
    # TE_test=(TE[800:])

    logreg=linear_model.LogisticRegression()
    # reg=linear_model.LinearRegression()
    # scores = cross_val_score(logreg, local_g, TE, cv=5)
    # print(str(scores)+' mean score: %.3f' % np.mean(scores))
    #logreg.fit(local_train, TE_train)
    kf = cross_validation.KFold(len(y), n_folds=5)
    avg_accuracy=0
    avg_falsepos=0
    avg_falseneg=0
    avg_corr_pos=0
    avg_corr_neg=0
    for train_index, test_index in kf:

       X_train, X_test = local_g[:int(.7*len(local_g))], local_g[int(.7*len(local_g)):]
       y_train, y_test = TE[:int(.7*len(local_g)),], TE[int(.7*len(local_g)):,]

       logreg.fit(X_train, y_train)
       g_ranking=(np.argsort(-np.std(X_test, 0)*logreg.coef_)[:3][0][:5])
       #print("STD: "+str(np.std(X_test, 0)*logreg.coef_))
       avg_accuracy+=accuracy_score(y_test, logreg.predict(X_test))
       confs=confusion_matrix(y_test, logreg.predict(X_test))
       avg_falseneg+=confs[0][1]/sum(confs[0])
       avg_falsepos+=confs[1][0]/sum(confs[1])
       avg_corr_pos+=confs[1][1]/(confs[0][1]+confs[1][1])
       avg_corr_neg+=confs[0][0]/(confs[1][0]+confs[0][0])

    #print(avg_falsepos/5)
    #print(avg_falseneg/5)
    print("5 Most Important Graphlets: "+str(g_ranking))
    print("Mean Accuracy: "+str(avg_accuracy/5))
    print(confs)
    #print("Mean Negative Classification Accuracy: "+str(avg_corr_neg/5))
    #print("Mean Positive Classification Accuracy: "+str(avg_corr_pos/5))
    #reg.fit(local_train,TE_train)
    #test_predicts=reg.predict(local_test)
    # print('Variance score: %.2f' % r2_score(TE_test, test_predicts))
    #plt.semilogy(test_predicts,TE_test,'r+')
    #plt.show()

#cascade_dist("dolphins/dolphin_ic.txt")
data="socfb-Reed98"
test=[6,7,9,10,11]
for i in range(1,4):
    #print("Subgraph, k="+str(i))
    #lin_reg(str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(i)+".txt",str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(i)+".txt")
    print("Single Node, k="+str(test[i]))
    lin_reg(str(data)+"/singleNode_logistic/"+str(data)+"_Xwave"+str(i)+".txt",str(data)+"/singleNode_logistic/"+str(data)+"_Ywave"+str(i)+".txt")

#graphlet_sig(str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(2)+".txt",str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(2)+".txt")
# lin_reg("dolphins/subGraphs_logistic/dolphin_Xwavesub0.txt","dolphins/subGraphs_logistic/dolphin_Ywavesub0.txt")
# lin_reg("dolphins/subGraphs_logistic/dolphin_Xwavesub1.txt","dolphins/subGraphs_logistic/dolphin_Ywavesub1.txt")
# lin_reg("dolphins/subGraphs_logistic/dolphin_Xwavesub2.txt","dolphins/subGraphs_logistic/dolphin_Ywavesub2.txt")
# lin_reg("dolphins/subGraphs_logistic/dolphin_Xwavesub3.txt","dolphins/subGraphs_logistic/dolphin_Ywavesub3.txt")
# lin_reg("dolphins/subGraphs_logistic/dolphin_Xwavesub4.txt","dolphins/subGraphs_logistic/dolphin_Ywavesub4.txt")
