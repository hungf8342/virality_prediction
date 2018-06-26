import sys
sys.path.insert(0, '../')
import graph_manip.shuffleGraphs as sg
import numpy as np
import numpy.random as nr
import networkx as nx
import scipy.stats as stats

data="socfb-Reed98"

def main():
    gDat = open("orig_graphs/socfb-Reed98.mtx", 'rb')
    firstLine = gDat.readline().split()
    graph = nx.read_edgelist(gDat)
    mu, sigma= 0.4, 0.2
    X=stats.truncnorm((0-mu)/sigma,(1-mu)/sigma,loc=mu,scale=sigma)
    weights=X.rvs(len(graph.edges))
    #weights=np.random.normal(0.8,0.1,len(graph.edges))
    c=[[1,2,3,4,5]]
    for i in range(100):
        nx.double_edge_swap(graph,10000,100000)
        filename = str(data)+"/graphs/"+str(data)+"_s_" + str(i) + ".dat"
        filename_w=str(data)+"/weight/"+str(data)+"_s_"+str(i) +".dat"
        output = [firstLine]
        nr.shuffle(weights)
        #random.shuffle(c)
        #print(shuffled_w)
        complete=[]

        #print(graph)
        print(nx.generate_edgelist(graph))
        t=0
        for line in nx.generate_edgelist(graph):
            vals = line.split()
            #print(i)
            #print(weights[i])
            complete.append([int(vals[0]), int(vals[1]), weights[t]])
            output.append([int(vals[0]), int(vals[1])])
            t+=1
        np.savetxt(open(filename_w,'wb'),complete,fmt="%s")
        np.savetxt(open(filename,'wb'), output, fmt="%s")

        print(filename)

main()
