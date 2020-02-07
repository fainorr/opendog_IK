
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

# call specific laser scan file
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

	# --- PROCESS SCAN DATA ---
	# pull text file into a vector "strings" with the laser scan message
	# at each point in time as a list

	strings = []

	with open(scan_data) as f:
		for line_num, line in enumerate(f):
			if line_num > 0:
				strings.append(line)

	# for each point in time, separate laser scan message into integer values
	# index i (rows) for time and index j (columns) for laser scan value

	msg_values = strings[0].count(',')+1
	num_samples = len(strings)

	laser_scan = [[0]*msg_values]*num_samples

	for i in range(0,num_samples):
		laser_scan[i][:] = strings[i].split(',')

	for i in range(0,num_samples):
		for j in range(0,msg_values):
			if j == 3:
				laser_scan[i][j] = 0
			else:
				laser_scan[i][j] = float(laser_scan[i][j])

	# extract angle and range values from laser_scan

	time = zeros(num_samples)
	angle_min = laser_scan[1][4]
	angle_max = laser_scan[1][5]
	angle_incr = laser_scan[1][6]
	# angles = arange(angle_min, angle_max, angle_incr)

	angles = zeros(360)
	distances = [[0]*msg_values]*360

	for i in range(0,num_samples):
		time[i] = i/10.0
		distances[i][:] = laser_scan[i][11:371]

	for i in range(0,num_samples):
		for j in range(0,360):
			if distances[i][j] == inf: distances[i][j] = 0.0

	for j in range(0,360):
		angles[j] = angle_min + angle_incr*j


	# --- CONVERT TO X,Y ---

	x_pos = [[0]*msg_values]*360
	y_pos = [[0]*msg_values]*360

	for i in range(0,len(angles)):
		for j in range(0,360):
			x_pos[i][j] = distances[i][j]*cos(angles[j])
			y_pos[i][j] = distances[i][j]*sin(angles[j])


	# --- PLOT SCAN ---

	if plot_in == "polar":
		fig = plt.figure()
		ax = fig.add_subplot(111, polar=True)
		c = ax.scatter(angles, distances[1][:])
		plt.axes(projection='polar')
		ax.set_rlim(0,2)
		fig.patch.set_facecolor('w')

	if plot_in == "cartesian":
		fig = plt.figure()
		ax = fig.add_subplot(111)
		c = ax.scatter(x_pos[1][:], y_pos[1][:])
		fig.patch.set_facecolor('w')

	plt.show()
