import numpy as np
import networkx as nx

def propagate(i,theta,E,T):
    l=E[E[:,0]==i,1]
    N=len(l)
    if N>0:
        v=np.random.rand(N)<theta
        l=l[v]
    T=T+len(l)
    return [l,T]
    
def eToA(E):
    A = np.zeros((np.max(E), np.max(E)))
    for i in range(E.shape[0]):
        A[E[i,0] - 1, E[i,1] - 1] = 1;
        A[E[i,1] - 1, E[i,0] - 1] = 1;

    return A

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

def exact_hawkes(G, max_gen, theta):
    A = nx.to_numpy_array(G)
    e, V = np.linalg.eig(A)
    if min(e) * theta <= -1 or max(e) * theta >= 1:
        return -1
    D = np.diag(e) * theta
    D = 1.0 / (1.0-D) - 1.0
    M = np.dot(np.dot(V, D), np.linalg.inv(V))
    N = A.shape[0];
    T = np.mean(M) * N + 1
    return T.real
