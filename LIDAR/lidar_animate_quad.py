
# Plot lidar data in and analyze in quadrants for obstacles

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import _color_data
from matplotlib.animation import FFMpegWriter

# call specific laser scan file
scan_data = 'LIDAR/hallway234.txt'

# CHOOSE ANALYSIS METHOD as "quadrant" or "intensity"
method = "intensity"


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

r_pos = zeros(360)
a_pos = zeros(360)

for i in range(0,num_samples):
	x_pos_now = []
	y_pos_now = []

	r_now = []

	for j in range(0,360):

		x_pos_now = append(x_pos_now,laser_scan[i][j+11]*cos(angles[j]))
		y_pos_now = append(y_pos_now,laser_scan[i][j+11]*sin(angles[j]))

		r_now = append(r_now,laser_scan[i][j+11])

	x_pos = vstack((x_pos,x_pos_now))
	y_pos = vstack((y_pos,y_pos_now))

	r_pos = vstack((r_pos,r_now))
	a_pos = vstack((a_pos,angles))


# --- ANALYZE SCAN ---

obst_size = 4           # number of consecutive dots
safe_range = 1.5        # search ranges for obstacles

quad_obstacles = zeros((num_samples,4))
obst_intensity = zeros((num_samples,4))

for i in range(0,num_samples):
	distances = zeros(360)

	for j in range(0,len(distances)):
	    if r_pos[i][j] > safe_range: distances[j] = 0
	    else: distances[j] = 1

	# reorder distances vector to reflect quadrants of interest
	distances[0:45] = distances[315:360]
	distances[46:360] = distances[0:314]

	if method == "quadrant":
		for quad in range(0,4):
		    quad_check = zeros((90-obst_size,1))

		    for j in range(90*quad, 90*(quad+1) - obst_size):
		        scan_obst_size = 0

		        for k in range(0,obst_size):
		            if distances[j+k] == 1: scan_obst_size = scan_obst_size + 1

		        if scan_obst_size == obst_size: quad_check[j-90*quad] = 1

		    if sum(quad_check >= 1): quad_obstacles[i][quad] = 1

	elif method == "intensity":
		quad_points = [0.,0.,0.,0.]
		for quad in range(0,4):
			for j in range(90*quad, 90*(quad+1)):
				if distances[j] == 1: quad_points[quad] = quad_points[quad] + 1

		obst_intensity[i] = quad_points/sum(quad_points)


# --- PREPARE FOR PLOT ---

ref_1x = [-10,10]
ref_1y = [-10,10]
ref_2x = [-10,10]
ref_2y = [10,-10]

circle_r = safe_range*ones(720)
circle_a = arange(0,360,0.5)
circle_x = zeros(len(circle_r))
circle_y = zeros(len(circle_r))

for i in range(0,len(circle_r)):
	circle_x[i] = circle_r[i]*cos(circle_a[i])
	circle_y[i] = circle_r[i]*sin(circle_a[i])

# make an array of all the points within the safe_range

x_pos_close = zeros(shape(x_pos))
y_pos_close = zeros(shape(y_pos))

for i in range(0,num_samples):
	m = 0

	for j in range(0,360):

		if r_pos[i][j] < safe_range:
			x_pos_close[i][m] = x_pos[i][j]
			y_pos_close[i][m] = y_pos[i][j]
			m = m+1


# --- ANIMATION FIGURE ---

fig = plt.figure(figsize=(6,6))
plt.axis('equal')
fig.patch.set_facecolor('w')
ax = plt.axes(xlim=(-10,10),ylim=(-10,10))

scatter = ax.scatter([],[],s=5,c='xkcd:light navy')
scatter_close = ax.scatter([],[],s=5,c='xkcd:scarlet')
ref_1, = ax.plot([],[],lw=1,c='xkcd:bluish grey',ls='--')
ref_2, = ax.plot([],[],lw=1,c='xkcd:bluish grey',ls='--')
range_circle, = ax.plot([],[],lw=1,c='xkcd:scarlet',ls='--')

front_list = []
right_list = []
back_list = []
left_list = []

def init():
	scatter.set_offsets(c_[x_pos[0][:],y_pos[0][:]])
	scatter_close.set_offsets(c_[x_pos_close[0][:],y_pos_close[0][:]])
	ref_1.set_data([], [])
	ref_2.set_data([], [])
	range_circle.set_data([], [])
	return(scatter, scatter_close, ref_1, ref_2, range_circle)

def animate(i):
	scatter.set_offsets(c_[x_pos[i][:],y_pos[i][:]])
	scatter_close.set_offsets(c_[x_pos_close[i][:],y_pos_close[i][:]])
	ref_1.set_data(ref_1x, ref_1y)
	ref_2.set_data(ref_2x, ref_2y)
	range_circle.set_data(circle_x, circle_y)

	# create annotations with live updates about quadrants

	if method == "quadrant":
		front_text = "front: {:.0f}".format(quad_obstacles[i][3])
		right_text = "right: {:.0f}".format(quad_obstacles[i][2])
		back_text = "back: {:.0f}".format(quad_obstacles[i][1])
		left_text = "left: {:.0f}".format(quad_obstacles[i][0])

	elif method == "intensity":
		front_text = "front: {:.2f}".format(obst_intensity[i][3])
		right_text = "right: {:.2f}".format(obst_intensity[i][2])
		back_text = "back: {:.2f}".format(obst_intensity[i][1])
		left_text = "left: {:.2f}".format(obst_intensity[i][0])

	for j, a in enumerate(front_list): a.remove()
	for j, a in enumerate(right_list): a.remove()
	for j, a in enumerate(back_list): a.remove()
	for j, a in enumerate(left_list): a.remove()

	front_list[:] = []
	right_list[:] = []
	back_list[:] = []
	left_list[:] = []

	front_ann = plt.annotate(front_text, xy=(0, 0), xytext=(0.5, 0.95), textcoords='axes fraction',
            horizontalalignment='center', verticalalignment='top')

	right_ann = plt.annotate(right_text, xy=(0, 0), xytext=(0.85, 0.5), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	back_ann = plt.annotate(back_text, xy=(0, 0), xytext=(0.5, 0.1), textcoords='axes fraction',
            horizontalalignment='center', verticalalignment='top')

	left_ann = plt.annotate(left_text, xy=(0, 0), xytext=(0.05, 0.5), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	front_list.append(front_ann)
	right_list.append(right_ann)
	back_list.append(back_ann)
	left_list.append(left_ann)

	return(scatter, scatter_close, ref_1, ref_2, range_circle)


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = num_samples, interval = 5, blit=False)

plt.show()
