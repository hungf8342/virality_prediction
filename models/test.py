import hawkes_sample as hs
import numpy as np

E = np.loadtxt("karate.txt", dtype='int')
TE = hs.exact_hawkes(E, 100, 0.1)
TS = hs.sample_hawkes(E, 1000, 0.1)
print(TE)
print(TS)
