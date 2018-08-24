import subprocess
import numpy as np
import networkx as nx
import csv
import os, sys
import random
sys.path.insert(0, '../../')
import models.indep_cascade as ic
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import re
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, roc_auc_score
from sklearn import datasets, linear_model, cross_validation
import _pickle as cPickle

#inputs: x-values file, y-values file, count file
#divide counts and counts into train/test data
def train_test(features,cases,count):
    trainx,testx=features[:int(.7*len(features))], features[int(.7*len(features)):]
    if features.ndim==1:
        trainx,testx=np.reshape(trainx,(-1,1)),np.reshape(testx,(-1,1))
    trainy, testy = cases[:int(.7*len(features)),], cases[int(.7*len(features)):,]
    traincount, testcount=count[:int(.7*len(features)),], count[int(.7*len(features)):,]
    return trainx,trainy,traincount,testx,testy,testcount

#inputs: x-values file, y-values file, count file, save file path, Degree vs. Graphlet label, and k test values
#run logistic regression and save AUC values in a file
def reg(x,y,counts,save,type,k):
    local_g=np.loadtxt(x)
    TE=np.loadtxt(y)
    counts=np.loadtxt(counts)
    logreg=linear_model.LogisticRegression()
    kf = cross_validation.KFold(len(y), n_folds=5)
    for train_index, test_index in kf:
        X_train, y_train,count_train,X_test,y_test,count_test = train_test(local_g,TE,counts)
        if (np.sum(y_train)) in [len(y_train),0] or (np.sum(y_test)) in [len(y_test),0]:
            return(None)
        else:
            logreg.fit(X_train, y_train)
            preds = logreg.predict_proba(X_test)
            roc_auc_score(y_test,preds[:,1])
            file_save=save+"reg.txt"
            with open(file_save, "a") as myfile:
                myfile.write(str(roc_auc_score(y_test,preds[:,1]))+'\n')
    return 2

#input: data name (str) and k test values (array of ints)
#find and save degree and graphlet AUC files 5 times
def update(data,test):
    for i in range(5):
        reg("../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Xwavesub"+str(i)+".txt",
            "../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_Ywavesub"+str(i)+".txt",
            "../data/"+str(data)+"/subGraphs_logistic/"+str(data)+"_count"+str(i)+".txt",
            "../data/"+str(data)+"/rocGraphs/"+str(test[i])+str(data),"Graphlets",test[i])
        reg("../data/"+str(data)+"/cent/"+str(data)+"_Xwave"+str(i)+".txt",
            "../data/"+str(data)+"/cent/"+str(data)+"_Ywave"+str(i)+".txt",
            "../data/"+str(data)+"/cent/"+str(data)+"_count"+str(i)+".txt",
            "../data/"+str(data)+"/centROC/"+str(test[i])+str(data),"Degree",test[i])
#graph_dist("Haverford-31",[5,10,15,20,25])
