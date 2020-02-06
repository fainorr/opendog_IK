
# Plot lidar-like data in polar coordinates

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt

# define the distance by "lidar scan" or by "random vector"
set_distances_by = "lidar scan"

# specify the type of plot as "polar" or "cartesian"
plot_in = "cartesian"

# specify if the scan data is one "snapshot" in time or "continuous"
scan_type = "continuous"

# call specific laser can file
scan_data = 'LIDAR/hallway234.txt'


if scan_type == "snapshot":

	# --- PROCESS SCAN DATA ---

	angles = arange(-pi, pi, pi/180)

	if set_distances_by == "lidar scan":

		distances = zeros(len(angles))
		with open('LIDAR/lidar_sample_scan.txt', 'r') as f:
			distances = f.read().split(', ')

		for i in range(0,len(angles)):
			distances[i] = round(float(distances[i]),5)
			if distances[i] == inf: distances[i] = 0.0


	if set_distances_by == "random vector":
		distances = zeros(len(angles))
		distances[0] = 20

		for i in range(1,len(angles)):
			distances[i] = distances[i-1] + random.normal(0,1)
			if distances[i]<0.0: distances[i] = 0.0


	# --- CONVERT TO X,Y ---

	x_pos = zeros(len(angles))
	y_pos = zeros(len(angles))

	for i in range(0,len(angles)):
		x_pos[i] = distances[i]*cos(angles[i])
		y_pos[i] = distances[i]*sin(angles[i])


	# --- PLOT SCAN ---

	if plot_in == "polar":
		fig = plt.figure()
		ax = fig.add_subplot(111, polar=True)
		c = ax.scatter(angles, distances)
		plt.axes(projection='polar')
		ax.set_rlim(0,2)
		fig.patch.set_facecolor('w')

	if plot_in == "cartesian":
		fig = plt.figure()
		ax = fig.add_subplot(111)
		c = ax.scatter(x_pos, y_pos)
		fig.patch.set_facecolor('w')

	plt.show()


if scan_type == "continuous":

	angles = arange(-pi, pi, pi/180)
	distances = zeros(len(angles))

	with open(scan_data, 'r') as f:
		for line_num, line in enumerate(f):
			if line_num>0
			time[line_num]
			print("Line {}: {}".format(line_num, line))

			#distances = f.readline().split(', ')
