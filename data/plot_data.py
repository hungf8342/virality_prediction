import sklearn.linear_model as lm
import pickle
import numpy as np
import matplotlib.pyplot as plt


D = pickle.load(open("outDataLocal.dat", "rb"))

xData = np.asarray(D[0])
yData = np.log10(np.asarray(D[1]))

inds = yData.argsort()

sortX = xData[inds]
sortY = yData[inds]

model = lm.LinearRegression()
model.fit(xData, yData)
print(model.score(xData, yData))
print(model.coef_)
plt.plot(model.predict(sortX), "r.", alpha=0.01)
plt.plot(sortY, "b-")
plt.show()
