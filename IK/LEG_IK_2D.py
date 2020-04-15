
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FFMpegWriter

# -----------------------
# INVERSE KINEMATICS: 2-D
# -----------------------

# robot dimensions
lf = 2.70 # femur, inches
lt = 2.60 # tibia, inches
ls = 5.00 # spine, inches

# establish gait parameters
gait_duration = 2 # seconds
leg_pace = 25 # pace of gait

# x-position of foot, moving in the range x_center +- x_stride
x_center = 0
x_stride = 0.5

# z-postion of foot, moving in the range z_center +- z_lift
z_center = -3
z_lift = 0.5

# phase shifts of each leg
leg1_offset = 0			# front left
leg2_offset = pi		# front right
leg3_offset = pi		# back left
leg4_offset = 0 		# back right


# initialize: x and z positions for each foot & femur and tibia angles for each leg
# leg indexing: 1-front left, 2-front right, 3-back left, 4-back right

t = linspace(0,gait_duration,1000)

x1 = zeros(len(t))
z1 = zeros(len(t))
angf1 = zeros(len(t))
angt1 = zeros(len(t))

x2 = zeros(len(t))
z2 = zeros(len(t))
angf2 = zeros(len(t))
angt2 = zeros(len(t))

x3 = zeros(len(t))
z3 = zeros(len(t))
angf3 = zeros(len(t))
angt3 = zeros(len(t))

x4 = zeros(len(t))
z4 = zeros(len(t))
angf4 = zeros(len(t))
angt4 = zeros(len(t))


# find foot positions for given gait at each point in time

for i in range(0,len(t)):
	x1[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg1_offset)
	z1[i] = z_center + z_lift*sin(leg_pace*t[i] - leg1_offset)

	x2[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg2_offset)
	z2[i] = z_center + z_lift*sin(leg_pace*t[i] - leg2_offset)

	x3[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg3_offset)
	z3[i] = z_center + z_lift*sin(leg_pace*t[i] - leg3_offset)

	x4[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg4_offset)
	z4[i] = z_center + z_lift*sin(leg_pace*t[i] - leg4_offset)


# ---------------------------
# INVERSE KINEMATICS FUNCTION
# ---------------------------

#  to solve for servo angles Af (femur) and At (tibia)

def getServoAng(x, z, lf, lt):
	if (x<0):
		Ad = arctan(z/x)
	else:
		Ad = pi + arctan(z/x)

	d = sqrt(x**2 + z**2)

	Af = Ad - arccos((lf**2 + d**2 - lt**2)/(2*lf*d))
	At = pi - arccos((lf**2 + lt**2 - d**2)/(2*lf*lt))

	return Af,At


# ANIMATION FIGURE

fig = plt.figure()
plt.axis('equal')
fig.patch.set_facecolor('w')
ax = plt.axes(xlim=(-(lf+lt)-ls,(lf+lt)), ylim=(-(lf+lt),(lf+lt)))

fline1, = ax.plot([],[],lw=5,c='0.7')
tline1, = ax.plot([],[],lw=5,c='0.7')
target1, = ax.plot([],[],lw=5,c='b')

fline3, = ax.plot([],[],lw=5,c='0.7')
tline3, = ax.plot([],[],lw=5,c='0.7')
target3, = ax.plot([],[],lw=5,c='0.7')

spine, = ax.plot([],[],lw=8,c='0.5')

fline2, = ax.plot([],[],lw=6,c='k')
tline2, = ax.plot([],[],lw=6,c='k')
target2, = ax.plot([],[],lw=6,c='k')

fline4, = ax.plot([],[],lw=6,c='k')
tline4, = ax.plot([],[],lw=6,c='k')
target4, = ax.plot([],[],lw=6,c='k')

x_ann_list = []
z_ann_list = []
Af_ann_list = []
At_ann_list = []

ax.legend([fline1, fline2], ['left legs', 'right legs'], loc='upper right')


def init():

	spine.set_data([],[])

	fline1.set_data([],[])
	tline1.set_data([],[])
	target1.set_data([],[])

	fline2.set_data([],[])
	tline2.set_data([],[])
	target2.set_data([],[])

	fline3.set_data([],[])
	tline3.set_data([],[])
	target3.set_data([],[])

	fline4.set_data([],[])
	tline4.set_data([],[])
	target4.set_data([],[])

	return fline1, tline1, target1, fline2, tline2, target2, fline3, tline3, target3, fline4, tline4, target4, spine


def animate(i):

	# solve for angles for each leg

	angf1[i], angt1[i] = getServoAng(x1[i], z1[i], lf, lt)
	angf2[i], angt2[i] = getServoAng(x2[i], z2[i], lf, lt)
	angf3[i], angt3[i] = getServoAng(x3[i], z3[i], lf, lt)
	angf4[i], angt4[i] = getServoAng(x4[i], z4[i], lf, lt)

	# ----------------------------
	# FORWARD KINEMATICS EQUATIONS
	# ----------------------------

	# calculate the limb positions for simulation, stored as endpoints of each element

	xf1 = [0, -lf*cos(angf1[i])]
	zf1 = [0, -lf*sin(angf1[i])]
	xt1 = [xf1[1], xf1[1] - lt*cos(angt1[i] + angf1[i])]
	zt1 = [zf1[1], zf1[1] - lt*sin(angt1[i] + angf1[i])]
	xtg1 = [x1[i], x1[i]]
	ztg1 = [z1[i], z1[i]]

	xf2 = [0, -lf*cos(angf2[i])]
	zf2 = [0, -lf*sin(angf2[i])]
	xt2 = [xf2[1], xf2[1] - lt*cos(angt2[i] + angf2[i])]
	zt2 = [zf2[1], zf2[1] - lt*sin(angt2[i] + angf2[i])]
	xtg2 = [x2[i], x2[i]]
	ztg2 = [z2[i], z2[i]]

	xf3 = [-ls, -ls-lf*cos(angf3[i])]
	zf3 = [0, -lf*sin(angf3[i])]
	xt3 = [xf3[1], xf3[1] - lt*cos(angt3[i] + angf3[i])]
	zt3 = [zf3[1], zf3[1] - lt*sin(angt3[i] + angf3[i])]
	xtg3 = [x3[i]-ls, x3[i]-ls]
	ztg3 = [z3[i], z3[i]]

	xf4 = [-ls, -ls-lf*cos(angf4[i])]
	zf4 = [0, -lf*sin(angf4[i])]
	xt4 = [xf4[1], xf4[1] - lt*cos(angt4[i] + angf4[i])]
	zt4 = [zf4[1], zf4[1] - lt*sin(angt4[i] + angf4[i])]
	xtg4 = [x4[i]-ls, x4[i]-ls]
	ztg4 = [z4[i], z4[i]]


	# write calculated position to limb elements in figure

	fline1.set_data(xf1, zf1)
	tline1.set_data(xt1, zt1)
	target1.set_data(xtg1, ztg1)

	fline2.set_data(xf2, zf2)
	tline2.set_data(xt2, zt2)
	target2.set_data(xtg2, ztg2)

	fline3.set_data(xf3, zf3)
	tline3.set_data(xt3, zt3)
	target3.set_data(xtg3, ztg3)

	fline4.set_data(xf4, zf4)
	tline4.set_data(xt4, zt4)
	target4.set_data(xtg4, ztg4)

	spine.set_data([-ls,0],[0,0])


	# create annotations with live updates about foot position and joint angles (for leg 1)

	x_text = "target x: {:.1f}".format(xtg1[0])
	z_text = "target z: {:.1f}".format(ztg1[0])
	Af_text = "femur angle: {:.0f}".format(angf1[i]*180/pi)
	At_text = "tibia angle: {:.0f}".format(angt1[i]*180/pi)


	# remove previous annotations

	for j, a in enumerate(z_ann_list):
		a.remove()
	for j, a in enumerate(x_ann_list):
		a.remove()
	for j, a in enumerate(Af_ann_list):
		a.remove()
	for j, a in enumerate(At_ann_list):
		a.remove()

	x_ann_list[:] = []
	z_ann_list[:] = []
	Af_ann_list[:] = []
	At_ann_list[:] = []


	# apply annotations to figure

	x_ann = plt.annotate(x_text, xy=(0, 0), xytext=(0.1, 0.95), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	z_ann = plt.annotate(z_text, xy=(0, 0), xytext=(0.1, 0.9), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	Af_ann = plt.annotate(Af_text, xy=(0, 0), xytext=(0.1, 0.8), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	At_ann = plt.annotate(At_text, xy=(0, 0), xytext=(0.1, 0.75), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	x_ann_list.append(x_ann)
	z_ann_list.append(z_ann)
	Af_ann_list.append(Af_ann)
	At_ann_list.append(At_ann)


 	return fline1, tline1, target1, fline2, tline2, target2, fline3, tline3, target3, fline4, tline4, target4,


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()
