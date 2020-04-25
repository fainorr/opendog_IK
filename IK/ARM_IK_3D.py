
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
from mpl_toolkits import mplot3d

# --------------------------
# ARM INVERSE KINEMATICS 3-D
# --------------------------

# arm dimensions
L1 = 0.432 	# piece connected to base, inches
L2 = 0.540 	# middle piece, inches
L3 = 0.126 	# end/tip, inches

# speed of motion
pace = 12.0

# end-effector start location
x_start = L3+L2-L1
y_start = 0.0
z_start = 0.0

# button location
x_final = 0.5
y_final = 0.2
z_final = 0.5

theta = linspace(0,2*pi,101)
x = zeros(len(theta))
y = zeros(len(theta))
z = zeros(len(theta))
ang0 = zeros(len(theta))
ang1 = zeros(len(theta))
ang2 = zeros(len(theta))
ang3 = zeros(len(theta))

# -------------------------------------------
# set end-effector path at each point in time
# -------------------------------------------

for i in range(0,len(theta)):

	# the first motion aligns the arm in the same plane as the button by
	# rotating the base and moving the end-effector to the final z-position
	if theta[i] < pi/2:
		x[i] = x_start + (x_start*cos(arctan(y_final/x_final))-x_start)*sin(theta[i])
		y[i] = y_start + (x_start*sin(arctan(y_final/x_final))-y_start)*sin(theta[i])
		z[i] = z_start + (z_final-z_start)*sin(theta[i])

	# the second motion, now aligned to the button, moves only the wrist
	# and elbow joints to approach the button parallel with the floor
	elif (theta[i] >= pi/2) and (theta[i] < pi):
		x_mid = x_start + (x_start*cos(arctan(y_final/x_final))-x_start)
		y_mid = y_start + (x_start*sin(arctan(y_final/x_final))-y_start)

		x[i] = x_mid + (x_final-x_mid)*sin(theta[i]-pi/2)
		y[i] = y_mid + (y_final-y_mid)*sin(theta[i]-pi/2)
		z[i] = z_final

	# for simulation purposes, the arm will stay at the final position before
	# resetting itself
	elif theta[i] >= pi:
		x[i] = x_final
		y[i] = y_final
		z[i] = z_final

# ---------------------------
# INVERSE KINEMATICS FUNCTION
# ---------------------------

# to solve for joint angles at each point in time given the end-effector position and limb dimensions

def getServoAng(x, y, z, L1, L2, L3):

	d_xy = sqrt(x**2 + y**2)
	xp = d_xy

	if (x>0):
		Ad = arctan(z/(xp-L3))
	else:
		Ad = pi + arctan(z/(xp-L3))

	d_xz = sqrt((xp-L3)**2 + z**2)

	# base angle
	A0 = arcsin(y/d_xy)

	# shoulder angle
	A1 = Ad + arccos((L1**2 + d_xz**2 - L2**2)/(2*L1*d_xz))

	# elbow angle
	A2 = arccos((L1**2 + L2**2 - d_xz**2)/(2*L1*L2))

	# wrist angle (constrained so the end link is parallel with the ground)
	A3 = 2*pi - A1 - A2

	return A0,A1,A2,A3


# ----------------
# ANIMATION FIGURE
# ----------------

fig = plt.figure(figsize=(6,6))
fig.patch.set_facecolor('w')
ax = plt.axes(projection='3d')
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(0,1)

limb1, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
limb2, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
limb3, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
target, = ax.plot([],[],[],lw=5,c='xkcd:desert', marker="o")
button, = ax.plot([],[],[],lw=5,c='xkcd:slate', marker="s")

x_list = []
y_list = []
z_list = []
A0_list = []
A1_list = []
A2_list = []
A3_list = []

def init():

	limb1.set_data([],[])
	limb2.set_data([],[])
	limb3.set_data([],[])
	limb1.set_3d_properties([])
	limb2.set_3d_properties([])
	limb3.set_3d_properties([])

	target.set_data([x[0],y[0]])
	target.set_3d_properties(z[0])

	button.set_data([x_final,y_final])
	button.set_3d_properties(z_final)

	return limb1, limb2, limb3, target, button


def animate(i):

	# solve for angles using the defined function
	ang0[i], ang1[i], ang2[i], ang3[i] = getServoAng(x[i], y[i], z[i], L1, L2, L3)


	# ----------------------------
	# FORWARD KINEMATICS EQUATIONS
	# ----------------------------

	# calculate the limb positions for simulation, stored as endpoints of each element

	limb1_x = [0, L1*cos(ang1[i])*cos(ang0[i])]
	limb1_y = [0, L1*cos(ang1[i])*sin(ang0[i])]
	limb1_z = [0, L1*sin(ang1[i])]

	limb2_x = [limb1_x[1], limb1_x[1]+L2*cos(ang1[i]+ang2[i]-pi)*cos(ang0[i])]
	limb2_y = [limb1_y[1], limb1_y[1]+L2*cos(ang1[i]+ang2[i]-pi)*sin(ang0[i])]
	limb2_z = [limb1_z[1], limb1_z[1]+L2*sin(ang1[i]+ang2[i]-pi)]

	limb3_x = [limb2_x[1], limb2_x[1]+L3*cos(ang0[i])]
	limb3_y = [limb2_y[1], limb2_y[1]+L3*sin(ang0[i])]
	limb3_z = [limb2_z[1], limb2_z[1]]


	# write calculated position to limb elements in figure

	limb1.set_data(limb1_x, limb1_y)
	limb2.set_data(limb2_x, limb2_y)
	limb3.set_data(limb3_x, limb3_y)
	limb1.set_3d_properties(limb1_z)
	limb2.set_3d_properties(limb2_z)
	limb3.set_3d_properties(limb3_z)

	target.set_data([x[i],y[i]])
	target.set_3d_properties(z[i])

	button.set_data([x_final,y_final])
	button.set_3d_properties(z_final)


	# create annotations

	x_text = "x = {:.1f}".format(x[i])
	y_text = "y = {:.1f}".format(y[i])
	z_text = "z = {:.1f}".format(z[i])
	A0_text = "base angle = {:.1f}".format(ang0[i]*180/pi)
	A1_text = "shoulder angle = {:.1f}".format(ang1[i]*180/pi)
	A2_text = "elbow angle = {:.1f}".format(ang2[i]*180/pi)
	A3_text = "wrist angle = {:.1f}".format(ang3[i]*180/pi)

	for j, a in enumerate(x_list): a.remove()
	for j, a in enumerate(y_list): a.remove()
	for j, a in enumerate(z_list): a.remove()
	for j, a in enumerate(A0_list): a.remove()
	for j, a in enumerate(A1_list): a.remove()
	for j, a in enumerate(A2_list): a.remove()
	for j, a in enumerate(A3_list): a.remove()
	x_list[:] = []
	y_list[:] = []
	z_list[:] = []
	A0_list[:] = []
	A1_list[:] = []
	A2_list[:] = []
	A3_list[:] = []

	x_ann = plt.annotate(x_text, xy=(0, 0), xytext=(0.1, 0.95), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	y_ann = plt.annotate(y_text, xy=(0, 0), xytext=(0.1, 0.9), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	z_ann = plt.annotate(z_text, xy=(0, 0), xytext=(0.1, 0.85), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	A0_ann = plt.annotate(A0_text, xy=(0, 0), xytext=(0.6, 0.95), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	A1_ann = plt.annotate(A1_text, xy=(0, 0), xytext=(0.6, 0.9), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	A2_ann = plt.annotate(A2_text, xy=(0, 0), xytext=(0.6, 0.85), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	A3_ann = plt.annotate(A3_text, xy=(0, 0), xytext=(0.6, 0.8), textcoords='axes fraction',
			horizontalalignment='left', verticalalignment='top')

	x_list.append(x_ann)
	y_list.append(y_ann)
	z_list.append(z_ann)
	A0_list.append(A0_ann)
	A1_list.append(A1_ann)
	A2_list.append(A2_ann)
	A3_list.append(A3_ann)

	return limb1, limb2, limb3, target, button,


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = len(theta), interval = 1, blit=False)
plt.show()
