import numpy as np

#We store edges and weighted influence between nodes in a symmetric Nx3 matrix 
#We store nodes along with their random thresholds and aggregate activation energy in another
#Nx3 matrix.

#Pointers: set initial aggregate influences to 0.

#adds weighted influence of a newly active node to its neighbors
#inputs are the two Nx3 matrices, current active node, active list, and newly active list
def neighbor_update(edge_matrix,node_matrix,n,active,new_active):
    neighbors=edge_matrix[edge_matrix[:,0]==n,1:]
    now_active=[]
    for i in range(0,np.ma.size(neighbors,axis=0)):
        neigh_weight=neighbors[i,1]
        neighbor=neighbors[i,0]
        #updating the ith neighbor's aggregate activation energy
        node_matrix[node_matrix[:,0]==neighbor,2]=node_matrix[node_matrix[:,0]==neighbor,2]+neigh_weight
        #adding ith neigbor to newly activated list if activation energy exceeds threshold
        if node_matrix[node_matrix[:,0]==neighbor,1]<node_matrix[node_matrix[:,0]==neighbor,2] and neighbor not in active and neighbor not in new_active:
            now_active.append(neighbor)
    return node_matrix,now_active

#runs linear threshold model until completion
#inputs are the two Nx3 matrices, active list, and newly active list
def update_graph(edge_mat,node_mat,new_active,active):
    while len(new_active)>0:
        for n in new_active:
            node_mat,now_active=neighbor_update(edge_mat,node_mat,n,active,new_active)
            #add activated neighbors to newly active list
            if len(now_active)!=0:
                new_active=np.append(new_active,now_active)
            new_active=new_active[1:]
            if n not in active:
                active=np.append(active,n)
    return node_mat,new_active,active
        

#generates a random testing network with a given number of edges(size) and number of nodes(num_nodes)
def network_gen(size,num_nodes):
    m=np.vstack((np.random.randint(1,num_nodes,size=size),np.random.randint(1,num_nodes,size=size),np.random.rand(size,)))
    m=np.reshape(np.ravel(m),(3,size)).T
    for row in range(0,np.ma.size(m,axis=0)):
        if (m[row,1]==m[row,2]):
            m=np.delete(m,{row},axis=0)
    node_list=np.vstack((np.asarray(range(1,num_nodes+1)),np.random.rand(num_nodes),np.zeros(num_nodes)))
    return m,node_list.T
        
