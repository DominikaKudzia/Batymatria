import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
datagps = pd.read_csv('Wszystkie.csv')
print(datagps.head())
X = datagps['X'].to_list()
Y = datagps['Y'].to_list()
H = datagps['H'].to_list()

mean_H = np.mean(H)
mean_X = np.mean(X)
mean_Y = np.mean(Y)
spatial_query = [abs(H - mean_H) < 1]
ax = plt.axes(projection='3d')
ax.scatter(X, Y, H,c='r',s=0.01)

axes =plt.gca()
axes.set_zlim([150,210])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('H')
plt.show()