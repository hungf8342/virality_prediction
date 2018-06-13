import numpy as np

## linear threshold model
# E -- an edge-list (symmetric), i.e. an N-by-3 array, u, v, w
# A0 -- a list of initial active nodes (numpy array)
# nIter -- number of iteration
#
# return:
# len(A) -- number of active nodes after nIter
# A      -- active nodes after nIter
# I      -- inactive nodes after nIter
def ltm(E, A0, nIter): 
    A = A0 # active nodes
    I = np.setdiff1d(E[:,0], A) # inactive nodes
    for t in range(0, nIter):
        new_active = []
        #print("step %d" % t, A)
        for i in I:
            theta = np.random.rand()
            tot = calcb(i, E, A)
            if tot >= theta:
                new_active.append(i)
        new_active = np.array(new_active)
        A = np.union1d(A, new_active)
        I = np.setdiff1d(I, new_active)
    
    return len(A), A, I

def calcb(i, E, A): # calc the total weight of active neighbors of an inactive node i
    E1 = E[np.in1d(E[:,0], A), :] # select active rows
    return np.sum(E1[E1[:,1]==i, 2])
