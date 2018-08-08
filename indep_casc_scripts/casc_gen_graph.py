import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import numpy.random as nr
import networkx as nx
import scipy.stats as stats
import pandas as pd

def clean():
    data = pd.read_csv('../data/orig_graphs/soc-Haverford.txt', sep=" ", header=None)
    data.iloc[1:]=data.iloc[1:]-1

def gen(data,filename):
    gDat = open(filename, 'rb')
    firstLine = gDat.readline().split()
    graph = nx.read_edgelist(gDat)

    #initialize weights
    mu, sigma= 0.2, 0.3
    X=stats.truncnorm((0-mu)/sigma,(1-mu)/sigma,loc=mu,scale=sigma)
    weights=X.rvs(len(graph.edges))

    complete=[]
    filename_w="../data/"+str(data)+"/weight/"+str(data)+"_s_0.txt"
    t=0
    #make edges+weight file
    for line in nx.generate_edgelist(graph):
        vals = line.split()
        complete.append([int(vals[0]), int(vals[1]), weights[t]])
        t+=1
    complete=np.vstack(complete)
    print(complete)
    np.savetxt(filename_w,complete,fmt='%f')

#gen("Haverford-X10","../orig_graphs/soc-Haverford.txt")
