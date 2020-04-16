
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import _color_data

# -------------
# LIDAR COMPARE
# -------------

# for single-frame scans, compare three analysis techniques simultaneously

scan_data = 'LIDAR/compare_scans/fifth_floor_tintersect.txt'

obst_size = 5           # number of consecutive dots
safe_range = 1.5         # search ranges for obstacles


# -----------------
# PROCESS SCAN DATA
# -----------------

file = open(scan_data)

for line in file:
    r_pos = line.split(", ")

angles = zeros(len(r_pos))
angle_min = -3.12413907051
angle_incr = 0.0174532923847

for i in range(0,len(r_pos)):
    r_pos[i] = float(r_pos[i])
    angles[i] = angle_min + angle_incr*i

x_pos = zeros(len(r_pos))
y_pos = zeros(len(r_pos))

for i in range(0,len(r_pos)):
    x_pos[i] = r_pos[i]*cos(angles[i])
    y_pos[i] = r_pos[i]*sin(angles[i])


# ------------
# ANALYZE SCAN: via three analysis techniques
# ------------
# [left, back, right, front]

quad_obstacles =[0.,0.,0.,0.]
obst_percent = [0.,0.,0.,0.]
obst_intensity = [0.,0.,0.,0.]


# for analysis, reorder values into four quadrants

distances = zeros(len(r_pos))
in_range = zeros(len(r_pos))

distances[0:45] = r_pos[315:360]
distances[45:360] = r_pos[0:315]

for i in range(0,len(distances)):
    if distances[i] > safe_range: in_range[i] = 0
    else: in_range[i] = 1


# -------------------
# METHOD = "QUADRANT"
# -------------------

for quad in range(0,4):
    quad_values = zeros((90-obst_size,1))

    for i in range(90*quad, 90*(quad+1) - obst_size):
        scan_obst_size = 0

        for k in range(0,obst_size):
            if in_range[i+k] == 1: scan_obst_size = scan_obst_size + 1

        if scan_obst_size == obst_size: quad_values[i-90*quad] = 1

    if sum(quad_values >= 1): quad_obstacles[quad] = 1


# ------------------
# METHOD = "PERCENT"
# ------------------

quad_points = [0.,0.,0.,0.]

for quad in range(0,4):
    for i in range(90*quad, 90*(quad+1)):
        if in_range[i] == 1: quad_points[quad] = quad_points[quad] + 1

obst_percent = quad_points/sum(quad_points)*100


# --------------------
# METHOD = "INTENSITY"
# --------------------

quad_points = [0.,0.,0.,0.]

for quad in range(0,4):
    for i in range(90*quad, 90*(quad+1)):
        if distances[i] != inf:
            quad_points[quad] = quad_points[quad] + distances[i]**2

for quad in range(0,4):
    if quad_points[quad] > 0:
        obst_intensity[quad] = sum(quad_points)/quad_points[quad]
    else:
        obst_intensity[quad] = inf

total_obst_intensity = sum(obst_intensity)

for quad in range(0,4):
    obst_intensity[quad] = obst_intensity[quad]/total_obst_intensity*100


print(quad_obstacles)
print(obst_percent)
print(obst_intensity)

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

# make an array of all the points within the safe_range

x_pos_close = zeros(shape(x_pos))
y_pos_close = zeros(shape(y_pos))
m = 0

for i in range(0,len(r_pos)):

	if r_pos[i] < safe_range:
		x_pos_close[m] = x_pos[i]
		y_pos_close[m] = y_pos[i]
		m = m+1


# -------------
# CREATE FIGURE
# -------------

fig = plt.figure(figsize=(6,6))
fig.patch.set_facecolor('w')
ax = fig.add_subplot(111)
ax = plt.axes(xlim=(-10,10),ylim=(-10,10))

scatter = ax.scatter(x_pos, y_pos, s=4, c='xkcd:dull blue')
scatter_close = ax.scatter(x_pos_close, y_pos_close, s=6, c='xkcd:aquamarine')
ref_1 = ax.plot(ref_a, ref_a, lw=1, c='xkcd:bluish grey', ls='--')
ref_2 = ax.plot(ref_a, ref_b, lw=1, c='xkcd:bluish grey', ls='--')
range_circle = ax.plot(circle_x, circle_y, lw=1, c='xkcd:aquamarine', ls='--')


# add annotations

front_text1 = "boolean: {:.0f}".format(quad_obstacles[3])
right_text1 = "boolean: {:.0f}".format(quad_obstacles[2])
back_text1 = "boolean: {:.0f}".format(quad_obstacles[1])
left_text1 = "boolean: {:.0f}".format(quad_obstacles[0])

front_text2 = "percent: {:.0f}%".format(obst_percent[3])
right_text2 = "percent: {:.0f}%".format(obst_percent[2])
back_text2 = "percent: {:.0f}%".format(obst_percent[1])
left_text2 = "percent: {:.0f}%".format(obst_percent[0])

front_text3 = "intensity: {:.0f}%".format(obst_intensity[3])
right_text3 = "intensity: {:.0f}%".format(obst_intensity[2])
back_text3 = "intensity: {:.0f}%".format(obst_intensity[1])
left_text3 = "intensity: {:.0f}%".format(obst_intensity[0])


front_ann1 = plt.annotate(front_text1, xy=(0, 0), xytext=(0.5, 0.96), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)
front_ann2 = plt.annotate(front_text2, xy=(0, 0), xytext=(0.5, 0.92), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)
front_ann3 = plt.annotate(front_text3, xy=(0, 0), xytext=(0.5, 0.88), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)

right_ann1 = plt.annotate(right_text1, xy=(0, 0), xytext=(0.95, 0.54), textcoords='axes fraction',
        horizontalalignment='right', verticalalignment='top', fontsize=9)
right_ann2 = plt.annotate(right_text2, xy=(0, 0), xytext=(0.95, 0.5), textcoords='axes fraction',
        horizontalalignment='right', verticalalignment='top', fontsize=9)
right_ann3 = plt.annotate(right_text3, xy=(0, 0), xytext=(0.95, 0.46), textcoords='axes fraction',
        horizontalalignment='right', verticalalignment='top', fontsize=9)

back_ann1 = plt.annotate(back_text1, xy=(0, 0), xytext=(0.5, 0.14), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)
back_ann2 = plt.annotate(back_text2, xy=(0, 0), xytext=(0.5, 0.1), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)
back_ann3 = plt.annotate(back_text3, xy=(0, 0), xytext=(0.5, 0.06), textcoords='axes fraction',
        horizontalalignment='center', verticalalignment='top', fontsize=9)

left_ann1 = plt.annotate(left_text1, xy=(0, 0), xytext=(0.05, 0.54), textcoords='axes fraction',
        horizontalalignment='left', verticalalignment='top', fontsize=9)
left_ann2 = plt.annotate(left_text2, xy=(0, 0), xytext=(0.05, 0.5), textcoords='axes fraction',
        horizontalalignment='left', verticalalignment='top', fontsize=9)
left_ann3 = plt.annotate(left_text3, xy=(0, 0), xytext=(0.05, 0.46), textcoords='axes fraction',
        horizontalalignment='left', verticalalignment='top', fontsize=9)

plt.show()
