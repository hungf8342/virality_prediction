import numpy as np
import networkx as nx
import graph_manip.shuffleGraphs as sg 
from models.hawkes import exact_hawkes
import matplotlib.pyplot as plt
import pickle

graph = nx.read_edgelist("graphs/karate.txt")
degree = sorted([d for n, d in graph.degree()], reverse=True)

new_graph = sg.shuffle(graph, 100)
new_degree = sorted([d for n, d in new_graph.degree()], reverse=True)
print(nx.degree_assortativity_coefficient(graph))
print(nx.degree_assortativity_coefficient(new_graph))
print(nx.to_numpy_matrix(graph))
print(exact_hawkes(graph, 1000, 0.1))

assortativity = []
hawkes = []

for i in range(400):
    temp_graph = sg.shuffle(graph, 1000)
    e_hawkes = exact_hawkes(temp_graph, 10000, 0.14) 
    if e_hawkes < 1000000:
        assortativity.append(nx.degree_assortativity_coefficient(temp_graph))
        hawkes.append(e_hawkes)
        print(i)

pickle.dump((assortativity, hawkes), open("r_1000_s_1000_h_10000.dat", "wb"))

fig = plt.figure()
ax = plt.gca()

exact_hawkes(temp_graph, 1000, 0.2)
ax.scatter(assortativity, hawkes, alpha=0.2)
ax.set_yscale('log')
plt.ylabel("Hawkes number")
plt.xlabel("Assortativity")
plt.show()
