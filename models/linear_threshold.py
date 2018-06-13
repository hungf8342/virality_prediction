import numpy as np

#We store edges and weighted influence between nodes in a symmetric Nx3 matrix 
#We store nodes along with their thresholds and aggregate neighbors' influence in another
#Nx3 matrix.

#Pointers: set initial aggregate influences to 0.

#adds weighted influence of a newly active node to its neighbors
def neighbor_update(edge_matrix,node_matrix,n,active,new_active):
    neighbors=edge_matrix[edge_matrix[:,0]==n,1:]
    now_active=[]
    #weights=neighbors[:,1]
    n_inf=node_matrix[node_matrix[:,0]==n,2]
    for i in range(0,np.ma.size(neighbors,axis=0)):
        neigh_weight=neighbors[i,1]
        neighbor=neighbors[i,0]
        node_matrix[node_matrix[:,0]==neighbor,2]=node_matrix[node_matrix[:,0]==neighbor,2]+neigh_weight*n_inf
        if node_matrix[node_matrix[:,0]==neighbor,1]<node_matrix[node_matrix[:,0]==neighbor,2] and neighbor not in active and neighbor not in new_active:
            now_active.append(neighbor)
    return node_matrix,now_active
    
def update_graph(edge_mat,node_mat,new_active,active):
    while len(new_active)>0:
        for n in new_active:
            print("new active is "+str(new_active))
            print("n is "+str(n))
            node_mat,now_active=neighbor_update(edge_mat,node_mat,n,active,new_active)
            print("now active is "+str(now_active))
            if len(now_active)!=0:
                print(len(now_active))
                new_active=np.append(new_active,now_active)
            new_active=new_active[1:]
            print(new_active)
            active=np.append(active,n)
    return node_mat,new_active,active
        
