import numpy as np
## independent cascade model
# E is N-by-3 matrix u, v, w
# A0 is an array of initial active nodes
#
# return:
# len(A) -- number of active nodes
# A      -- a list of active nodes
def icascade(E, A0): 
    curr_A = A0 # current active nodes
    A = A0 # once active nodes
    while len(curr_A) > 0:
        i = curr_A[0]
        E1 = E[E[:,0] == i, :] # select neighbors
        E2 = E1[np.in1d(E1[:,1], A, invert=True), :] # select inactive rows
        N = len(E2)
        v = E2[:, 2] >= np.random.rand(N) # succeeds with probability w
        curr_A = np.append(curr_A[1:], E2[v, 1])
        A = np.append(A, E2[v, 1])
    
    return len(A), A
