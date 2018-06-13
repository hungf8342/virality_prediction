import numpy as np

# Calculates the degrees of the edges of a network
def getDegree(E):
    deg = np.zeros(np.max(E))
    for edge in E:
        deg[edge[0] - 1] += 1
    return deg

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
