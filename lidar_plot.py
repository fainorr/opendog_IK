
# Plot lidar-like data in polar coordinates

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt

angles = arange(-pi, pi, pi/45)
distances = zeros(len(angles))
distances[0] = 20

for i in range(1,len(angles)):
	distances[i] = distances[i-1] + random.normal(0,1)
	if distances[i]<0.0: distances[i] = 0.0

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
c = ax.scatter(angles, distances)
plt.axes(projection='polar')
fig.patch.set_facecolor('w')

plt.show()
