import numpy as np
import networkx as nx
import graph_manip.shuffleGraphs as sg 
from models.hawkes import exact_hawkes
import matplotlib.pyplot as plt
import pickle
import sklearn.linear_model as lm

graph = nx.read_edgelist("graphs/soc-dolphins_f.txt")

eig_coeff = 1/max(np.linalg.eig(nx.to_numpy_matrix(graph))[0])
print(eig_coeff*.96)
assortativity = []
hawkes = []

theta_scaled = .96

for i in range(10000):
    sg.shuffle(graph, 1)
    e_hawkes = exact_hawkes(graph, 10000, theta_scaled * eig_coeff)
    if(e_hawkes > 0):
        assortativity.append(nx.degree_assortativity_coefficient(graph))
        hawkes.append(e_hawkes)
        print(i)
    else:
        print(e_hawkes)

pickle.dump((assortativity, hawkes), open("r_1000_s_1000_h_10000.dat", "wb"))

model = lm.LinearRegression()
model.fit(np.asmatrix(assortativity).T, np.log10(hawkes))
print(model.score(np.asmatrix(assortativity).T, np.log10(hawkes)))

xpred = np.asmatrix(np.linspace(-.5, -.2, 1000)).T
ypred = (model.predict(xpred))

fig = plt.figure()
ax = plt.gca()

ax.scatter(assortativity, np.log10(hawkes), alpha=0.1)
ax.plot(xpred, ypred, 'r-')
#ax.set_yscale('log')
plt.ylabel("Hawkes number")
plt.xlabel("Assortativity")
plt.show()
