
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
# pull text file into an array "laser_scan" of integers
# laser_scan[i][j] where i = time and j = value within message

laser_scan = zeros(731)

with open(scan_data) as f:
	for line_num, line in enumerate(f):
		if line_num > 0:
			nums = []
			linestrip = line.strip()
			linesplit = line.split(',')
			for k in range(0,len(linesplit)):

				try:
					nums = append(nums,float(linesplit[k]))
				except:
					nums = append(nums,0)

			laser_scan = vstack((laser_scan,nums))

msg_values = len(laser_scan[0])
num_samples = len(laser_scan)

# extract angle values from laser_scan

angle_min = laser_scan[1][4]
angle_max = laser_scan[1][5]
angle_incr = laser_scan[1][6]

angles = zeros(360)

for j in range(0,360):
	angles[j] = angle_min + angle_incr*j


# --- CONVERT TO X,Y ---

x_pos = zeros(360)
y_pos = zeros(360)

for i in range(0,num_samples):
	x_pos_now = []
	y_pos_now = []

	for j in range(0,360):

		x_pos_now = append(x_pos_now,laser_scan[i][j+11]*cos(angles[j]))
		y_pos_now = append(y_pos_now,laser_scan[i][j+11]*sin(angles[j]))

	x_pos = vstack((x_pos,x_pos_now))
	y_pos = vstack((y_pos,y_pos_now))


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

ani = animation.FuncAnimation(fig, animate, init_func=init, frames = num_samples, interval = 5, blit=False)

plt.show()
