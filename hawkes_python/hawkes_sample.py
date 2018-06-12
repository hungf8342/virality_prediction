import matplotlib.pyplot as plt
import numpy as np

def propagate(i,theta,E,T):
    l=E[E[:,0]==i,1]
    N=len(l)
    if N>0:
        v=np.random.rand(N)<theta
        l=l[v]
    T=T+len(l)
    return [l,T]
    

def sample_hawkes (E,Nsamples,theta):
    N=len(np.unique(E[:,1]))
    T=np.ones(Nsamples)
    
    for k in range(0,Nsamples):
        i=np.random.randint(0,N)
        node_list=np.asarray([i])
        while len(node_list)>0:
            prop=propagate(node_list[0],theta,E,T[k])
            l=prop[0]
            T[k]=prop[1]
            node_list=node_list[1:]
            if len(l)!=0:
                node_list=np.append(node_list,l)
    T=np.mean(T)
    return T 
