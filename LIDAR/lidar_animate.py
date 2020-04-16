
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import _color_data
from matplotlib.animation import FFMpegWriter
from analysis_methods import *

# ---------------
# LIDAR ANIMATION
# ---------------

# analyze LIDAR data in four quadrants to identify obstacles and then animate scans
# to visualize the analysis techniques and understand how they change based on the raw data

# call specific laser scan file
scan_data = 'LIDAR/animate_scans/corner208.txt'

# CHOOSE ANALYSIS METHOD as "quadrant" or "percent" or "intensity"
method = "quadrant"

obst_size = 5            	# number of consecutive dots
safe_range = 2.0         	# search ranges for obstacles


# -----------------
# PROCESS SCAN DATA
# -----------------
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


# -------------------------
# PULL DATA FROM LASER SCAN
# -------------------------

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

	# stack onto previous times
	x_pos = vstack((x_pos,x_pos_now))
	y_pos = vstack((y_pos,y_pos_now))

	r_pos = vstack((r_pos,r_now))
	a_pos = vstack((a_pos,angles))


# ------------
# ANALYZE SCAN: via three analysis techniques
# ------------

quad_obstacles = zeros((num_samples,4))
obst_percent = zeros((num_samples,4))
obst_intensity = zeros((num_samples,4))

for i in range(0,num_samples):

	# for analysis, reorder values into four quadrants

	distances = zeros(len(r_pos[i]))
	in_range = zeros(len(r_pos[i]))

	distances[0:45] = r_pos[i][315:360]
	distances[45:360] = r_pos[i][0:315]

	# define a boolean array "in_range" which is 1 if the point is within the range

	for j in range(0,len(distances)):
	    if distances[j] > safe_range: in_range[j] = 0
	    else: in_range[j] = 1


	# method = "QUADRANT"
	if method == "quadrant":
		quad_obstacles[i][:] = analyze_quadrant(obst_size,in_range)

	# method = "PERCENT"
	elif method == "percent":
		obst_percent[i][:] = analyze_percent(in_range)

	# method = "INTENSITY"
	elif method == "intensity":
		safe_range = 15
		obst_intensity[i][:] = analyze_intensity(distances)


# ----------------
# PREPARE FOR PLOT
# ----------------

ref_a = [-10,10]
ref_b = [10,-10]

circle_r = safe_range*ones(720)
circle_a = arange(0,360,0.5)
circle_x = zeros(len(circle_r))
circle_y = zeros(len(circle_r))

for i in range(0,len(circle_r)):
	circle_x[i] = circle_r[i]*cos(circle_a[i])
	circle_y[i] = circle_r[i]*sin(circle_a[i])


# make an array of all the points within the safe_range to plot in a different color

x_pos_close = zeros(shape(x_pos))
y_pos_close = zeros(shape(y_pos))

for i in range(0,num_samples):
	m = 0

	for j in range(0,360):

		if r_pos[i][j] < safe_range:
			x_pos_close[i][m] = x_pos[i][j]
			y_pos_close[i][m] = y_pos[i][j]
			m = m+1


# ----------------
# ANIMATION FIGURE
# ----------------

fig = plt.figure(figsize=(6,6))
plt.axis('equal')
fig.patch.set_facecolor('w')
ax = plt.axes(xlim=(-10,10),ylim=(-10,10))

scatter = ax.scatter([],[],s=5,c='xkcd:light navy')
scatter_close = ax.scatter([],[],s=5,c='xkcd:yellow orange')
ref_1, = ax.plot([],[],lw=1,c='xkcd:bluish grey',ls='--')
ref_2, = ax.plot([],[],lw=1,c='xkcd:bluish grey',ls='--')
range_circle, = ax.plot([],[],lw=1,c='xkcd:yellow orange',ls='--')

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

	method_text = "method: {}".format(method)
	method_ann = plt.annotate(method_text, xy=(0, 0), xytext=(0.95, 0.95), textcoords='axes fraction',
			horizontalalignment='right', verticalalignment='top')
	return(scatter, scatter_close, ref_1, ref_2, range_circle)

def animate(i):
	scatter.set_offsets(c_[x_pos[i][:],y_pos[i][:]])
	scatter_close.set_offsets(c_[x_pos_close[i][:],y_pos_close[i][:]])
	ref_1.set_data(ref_a, ref_a)
	ref_2.set_data(ref_a, ref_b)
	range_circle.set_data(circle_x, circle_y)

	# create annotations with live updates about quadrants

	if method == "quadrant":
		front_text = "front: {:.0f}".format(quad_obstacles[i][3])
		right_text = "right: {:.0f}".format(quad_obstacles[i][2])
		back_text = "back: {:.0f}".format(quad_obstacles[i][1])
		left_text = "left: {:.0f}".format(quad_obstacles[i][0])

	elif method == "percent":
		front_text = "front: {:.0f}%".format(obst_percent[i][3])
		right_text = "right: {:.0f}%".format(obst_percent[i][2])
		back_text = "back: {:.0f}%".format(obst_percent[i][1])
		left_text = "left: {:.0f}%".format(obst_percent[i][0])

	elif method == "intensity":
		front_text = "front: {:.0f}%".format(obst_intensity[i][3])
		right_text = "right: {:.0f}%".format(obst_intensity[i][2])
		back_text = "back: {:.0f}%".format(obst_intensity[i][1])
		left_text = "left: {:.0f}%".format(obst_intensity[i][0])

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


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = num_samples, interval = 100, blit=False)

plt.show()
