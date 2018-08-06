import numpy as np
import networkx as nx


def loadGraph(filename):
    gDat = open(filename, 'rb')
    
    # Read the node and edge numbers
    firstLine = gDat.readline().split()
    
    # Load the rest of the data into a networkx network
    graph = nx.read_edgelist(gDat)
    return graph


# Calculates the degrees of the edges of a network
def getDegree(E):
    deg = np.zeros(np.max(E))
    for edge in E:
        deg[edge[0] - 1] += 1
    return deg

def eToA(E):
    A = np.zeros((np.max(E) + 1, np.max(E) + 1))
    for i in range(E.shape[0]):
        A[E[i,0], E[i,1]] = 1;
        A[E[i,1], E[i,0]] = 1;

    return A

def getCritTheta(G):
    A = nx.to_numpy_array(G)
    return 1/max(np.linalg.eig(A)[0])

def getCritThetaEdge(E):
    A = eToA(E)
    return 1/max(np.linalg.eig(A)[0])

# To calculate this, we use the Pearson Correlation Coefficient
# of degrees at either end of a network edge
def assortativity(E):
    M = E.shape[0]

    # First, we'll calculate relevant sums over the data
    prod = 0
    square_sum = 0
    sum_square = 0

    deg = getDegree(E)

    for edge in E:
        prod += deg[edge[0] - 1] * deg[edge[1] - 1]
        square_sum += deg[edge[0] - 1] + deg[edge[1] - 1]
        sum_square += deg[edge[0] - 1]**2 + deg[edge[1] - 1]**2

    # Then we use those in the assortativity equation
    numer = 1.0 / M * prod - (1.0 / M * 0.5 * square_sum )**2
    denom = 1.0 / M * 0.5 * sum_square - (1.0 / M * 0.5 * square_sum)**2
    assort = numer / denom

    return assort

def getThetaDist(G, num_shuffles, num_graphs, debug=False):
    data = []
    for i in range(num_graphs):
        
        nx.double_edge_swap(G, nswap=num_shuffles, max_tries=(10 * num_shuffles))
        data.append(getCritTheta(G))
        if debug:
            print i

    return data
