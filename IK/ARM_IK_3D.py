
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
from mpl_toolkits import mplot3d


# ARM INVERSE KINEMATICS 2-D

# arm dimensions

L1 = 16.0 	# piece connected to base, inches
L2 = 20.0 	# middle piece, inches
L3 = 5.0 	# end/tip, inches

gait_duration = 2 # seconds
pace = 25.0

d_poke = 10.0

x_final = 20.0
y_final = 5.0
z_final = 10.0

x_start = x_final - d_poke*cos(arctan(y_final/x_final))
y_start = y_final - d_poke*sin(arctan(y_final/x_final))

t = linspace(0,gait_duration,1000)
x = zeros(len(t))
y = zeros(len(t))
z = zeros(len(t))
ang0 = zeros(len(t))
ang1 = zeros(len(t))
ang2 = zeros(len(t))
ang3 = zeros(len(t))


for i in range(0,len(t)):
	x[i] = x_start + d_poke*sin(pace*t[i])*cos(arctan(y_final/x_final))
	if x[i] < x_start:
		x[i] = x_start

	y[i] = y_start + d_poke*sin(pace*t[i])*sin(arctan(y_final/x_final))
	if y[i] < y_start:
		y[i] = y_start

	z[i] = z_final


def getServoAng(x, y, z, L1, L2, L3):

	d_xy = sqrt(x**2 + y**2)
	A0 = arcsin(y/d_xy)

	xp = d_xy

	if (x>0):
		Ad = arctan(z/(xp-L3))
	else:
		Ad = pi + arctan(z/(xp-L3))

	d_xz = sqrt((xp-L3)**2 + z**2)

	A1 = Ad + arccos((L1**2 + d_xz**2 - L2**2)/(2*L1*d_xz))
	A2 = arccos((L1**2 + L2**2 - d_xz**2)/(2*L1*L2))
	A3 = 2*pi - A1 - A2

	return A0,A1,A2,A3


# ANIMATION FIGURE

fig = plt.figure(figsize=(6,6))
fig.patch.set_facecolor('w')
ax = plt.axes(projection='3d')
ax.set_xlim(-15,25)
ax.set_ylim(-20,20)
ax.set_zlim(0,40)

limb1, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
limb2, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
limb3, = ax.plot([],[],[],lw=5,c='xkcd:blue green')
target = ax.scatter([],[],[],s=100,c='xkcd:desert')
button = ax.scatter([],[],[],s=50,c='xkcd:slate', marker="s")

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
	target.set_offsets([x[0],y[0],z[0]])
	button.set_offsets([x_final,y_final,z_final])

	return limb1, limb2, limb3, target, button


def animate(i):

	# solve for angles and calculate the limb positions for simulation

	ang0[i], ang1[i], ang2[i], ang3[i] = getServoAng(x[i], y[i], z[i], L1, L2, L3)

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

	target.set_offsets([x[i],y[i],z[i]])
	button.set_offsets([x_final,y_final,z_final])


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


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()
