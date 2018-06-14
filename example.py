import networkx as nx
import graph_manip.shuffleGraphs as sg
import graph_manip.graphAttribs as ga
import models.hawkes as hk
import numpy as np
import matplotlib.pyplot as plt

# First, we show how the hawkes model runs on data

NUM_POINTS = 30

graph = nx.read_edgelist("graphs/karate.txt")
data = np.loadtxt("graphs/karate.txt", dtype='int')
theta = np.linspace(0, 0.14, NUM_POINTS)

exact = []
sample = []

for i in range(NUM_POINTS):
    exact.append(hk.exact_hawkes(graph, 100, theta[i]))
    sample.append(hk.sample_hawkes(data, 10000, theta[i]))


plt.plot(theta, exact)
plt.plot(theta, sample)

plt.show()
