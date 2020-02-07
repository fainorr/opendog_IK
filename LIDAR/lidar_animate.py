
# Plot lidar-like data in polar coordinates

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FFMpegWriter

# specify the type of plot as "polar" or "cartesian"
plot_in = "cartesian"

# call specific laser scan file
scan_data = 'LIDAR/hallway234.txt'


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
	laser_scan[i][:]

print(laser_scan[1][:])
print(laser_scan[4][:])

for i in range(0,num_samples):
	for j in range(0,msg_values):
		if j == 3:
			laser_scan[i][j] = 0
		else:
			laser_scan[i][j] = float(laser_scan[i][j])

print(laser_scan[1][11:])
print(laser_scan[4][11:])

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

for i in range(0,num_samples):
	for j in range(0,360):
		x_pos[i][j] = distances[i][j]*cos(angles[j])
		y_pos[i][j] = distances[i][j]*sin(angles[j])


# --- ANIMATION FIGURE ---

fig = plt.figure()
plt.axis('equal')
fig.patch.set_facecolor('w')
ax = plt.axes(xlim=(-10,10),ylim=(-10,10))
scatter = ax.scatter([],[],5)

def init():
	scatter.set_offsets(c_[x_pos[0][:],y_pos[0][:]])
	return(scatter)

def animate(i):
	scatter.set_offsets(c_[x_pos[i][:],y_pos[i][:]])
	return(scatter)

ani = animation.FuncAnimation(fig, animate, init_func=init, frames = num_samples, interval = 2, blit=False)

plt.show()
