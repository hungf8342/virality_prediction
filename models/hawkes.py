import numpy as np

# E is Nx2 array that contains the index of the edges.  Should be symmetric
# where if [i j] is a row then [j i] is also a row (and now duplicate rows)
#
# Nsamples is number of times to simulate branching process
# theta is the probability an event at a node triggers an event at neighbor
# output T is the total expected number of events

def propagate(i,theta,E,T):
    l=E[E[:,0]==i,1]
    N=len(l)
    if N>0:
        v=np.random.rand(N)<theta
        l=l[v]
    T=T+len(l)
    return l,T

def eToA(E):
    A = np.zeros((np.max(E), np.max(E)))
    print(A)
    for i in range(E.shape[0]):
        A[E[i,0] - 1, E[i,1] - 1] = 1;
        A[E[i,1] - 1, E[i,0] - 1] = 1;

    return A

##For each sample iteration, choose a random node where an event occurs.
##Propogate (spread an event to neighbors based on rate theta) from that node
##and add to the total expected number of events for that sample  iteration.
##Update the node list by removing the node we just propogated from and
##add the newly active nodes. Do so until the node list is empty. Move on to
##the next iteration.

def sample_hawkes (E,Nsamples,theta):
    N=len(np.unique(E[:,1]))
    T=np.ones(Nsamples)

    for k in range(0,Nsamples):
        i=np.random.randint(0,N)
        node_list=np.asarray([i])
        while len(node_list)>0:
            l, T[k]=propagate(node_list[0],theta,E,T[k])
            node_list=node_list[1:]
            if len(l)!=0:
                node_list=np.append(node_list,l)
    T=np.mean(T)
    return T

def exact_hawkes(E, max_gen, theta):
    A = eToA(E)
    M = np.zeros(A.shape)

    for i in xrange(1,max_gen):
        M = M + np.linalg.matrix_power(theta * A, i-1);


    N = A.shape[0];
    T = np.mean(M) * N
    return T
