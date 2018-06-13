import graph_manip.shuffleGraphs as sg
import graph_manip.graphAttribs as ga
import models.hawkes as hk
import numpy as np
import matplotlib.pyplot as plt

# First, we show how the hawkes model runs on data

NUM_POINTS = 100

data = np.loadtxt("graphs/karate.txt", dtype='int')
#theta = np.linspace(0, 0.14, NUM_POINTS)
#
#exact = []
#sample = []
#
#for i in range(NUM_POINTS):
#    exact.append(hk.exact_hawkes(data, 100, theta[i]))
#    sample.append(hk.sample_hawkes(data, 10000, theta[i]))
#    print(theta[i])

print(ga.assortativity(data))

#plt.plot(theta, exact)
#plt.plot(theta, sample)
#
#plt.show()
