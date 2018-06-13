import numpy as np

#In an Independent Cascade model, we have a network with preset probability values of an event 
#passing from one node to another. This means we must input a network (represented as a list of edges)
#and corresponding probability values (all in all, an N x 3 matrix).

#For each newly active node, we flip a weighted coin for each outgoing edge which determines 
#whether that neighbor becomes active or not. We repeat until there are no outgoing edges or 
#all nodes have been attempted to been reached. In this case, flipping coins can be done for
#all edges before we start the actual independent cascade process.

#flips a weighted coin given a winning (activation) probability
def coin_flip(win_p):
    i=np.random.rand()
    if i<win_p:
        return True
    return False

#predetermines based on edge probability whether a node will be activated if edge is encountered
#parameter is the Nx3 matrix of edges+probabilities, outputs an Nx4 matrix 
def make_matrix(data):
    poss_edges=[coin_flip(t) for t in data[:,2]]
    poss_edges=np.asarray([poss_edges]).T
    return np.hstack((data,poss_edges)).astype(int)

#implements independent cascade
#parameters are Nx3 matrix of edges & probabilities and a starting node, outputs final active nodes
def indep_casc(edges_probs,s):
    active=[]
    new_active=np.asarray([s]).astype(int)
    info_mat=make_matrix(edges_probs)
    #while there are still newly active nodes, find the oldest's neighbors
    while len(new_active)>0:
        n=new_active[0]
        neighbors=info_mat[info_mat[:,0]==n,1:]
        print("while new_active is not empty, loops= "+str(np.ma.size(neighbors,axis=0)))
        for i in range(0,np.ma.size(neighbors,axis=0)):
            print("Before "+str(new_active))
            print(str(n)+"'s neighbor "+str(neighbors[i,0])+" has truth value"+str(neighbors[i,2]))
            #if neighbor is conditionally connected via flip & inactive, add to newly active
            if neighbors[i,2]:
                if neighbors[i,0] not in active and neighbors[i,0] not in new_active:
                    new_active=np.append(new_active,int(neighbors[i,0]))
        new_active=new_active[1:]
        print("After "+str(new_active))
        active=np.append(active,n)
    return active
