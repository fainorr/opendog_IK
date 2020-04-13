from numpy import *
from math import *
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FFMpegWriter

# ARM INVERSE KINEMATICS 2-D

# arm dimensions

L1 = 16.0 	# piece connected to base, inches
L2 = 20.0 	# middle piece, inches
L3 = 5.0 	# end/tip, inches

gait_duration = 2 # seconds
x_start = 10.0
x_final = 20.0
x_pace = 25.0
z_final = 10.0

t = linspace(0,gait_duration,1000)
x = zeros(len(t))
z = zeros(len(t))
ang1 = zeros(len(t))
ang2 = zeros(len(t))
ang3 = zeros(len(t))


for i in range(0,len(t)):
	x[i] = x_start + (x_final-x_start)*sin(x_pace*t[i])
	if x[i] < x_start:
		x[i] = x_start

	z[i] = z_final


def getServoAng(x, z, L1, L2, L3):

	if (x>0):
	    Ad = arctan(z/(x-L3))
	else:
	    Ad = pi + arctan(z/(x-L3))

	d = sqrt((x-L3)**2 + z**2)

	A1 = Ad + arccos((L1**2 + d**2 - L2**2)/(2*L1*d))
	A2 = arccos((L1**2 + L2**2 - d**2)/(2*L1*L2))
	A3 = 2*pi - A1 - A2

	return A1,A2,A3


# ANIMATION FIGURE

fig = plt.figure(figsize=(6,6))
fig.patch.set_facecolor('w')
ax = plt.axes(xlim=(-15,25), ylim=(-0,40))

limb1, = ax.plot([],[],lw=5,c='xkcd:blue green')
limb2, = ax.plot([],[],lw=5,c='xkcd:blue green')
limb3, = ax.plot([],[],lw=5,c='xkcd:blue green')
target = ax.scatter([],[],s=100,c='xkcd:desert')
button = ax.scatter([],[],s=50,c='xkcd:slate', marker="s")

x_list = []
z_list = []
A1_list = []
A2_list = []
A3_list = []

def init():

	limb1.set_data([],[])
	limb2.set_data([],[])
	limb3.set_data([],[])
	target.set_offsets([x[0],z[0]])
	target.set_offsets([x_final,z_final])

	return limb1, limb2, limb3, target, button


def animate(i):

	# solve for angles and calculate the limb positions for simulation

	ang1[i], ang2[i], ang3[i] = getServoAng(x[i], z[i], L1, L2, L3)

	limb1_x = [0, L1*cos(ang1[i])]
	limb1_z = [0, L1*sin(ang1[i])]

	limb2_x = [limb1_x[1], limb1_x[1]+L2*cos(ang1[i]+ang2[i]-pi)]
	limb2_z = [limb1_z[1], limb1_z[1]+L2*sin(ang1[i]+ang2[i]-pi)]

	limb3_x = [limb2_x[1], limb2_x[1]+L3]
	limb3_z = [limb2_z[1], limb2_z[1]]


	# write calculated position to limb elements in figure

	limb1.set_data(limb1_x, limb1_z)
	limb2.set_data(limb2_x, limb2_z)
	limb3.set_data(limb3_x, limb3_z)
	target.set_offsets([x[i], z[i]])
	button.set_offsets([x_final,z_final])


	# create annotations

	x_text = "x = {:.1f}".format(x[i])
	z_text = "z = {:.1f}".format(z[i])
	A1_text = "shoulder angle = {:.1f}".format(ang1[i]*180/pi)
	A2_text = "elbow angle = {:.1f}".format(ang2[i]*180/pi)
	A3_text = "wrist angle = {:.1f}".format(ang3[i]*180/pi)

	for j, a in enumerate(x_list): a.remove()
	for j, a in enumerate(z_list): a.remove()
	for j, a in enumerate(A1_list): a.remove()
	for j, a in enumerate(A2_list): a.remove()
	for j, a in enumerate(A3_list): a.remove()
	x_list[:] = []
	z_list[:] = []
	A1_list[:] = []
	A2_list[:] = []
	A3_list[:] = []

	x_ann = plt.annotate(x_text, xy=(0, 0), xytext=(0.1, 0.95), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	z_ann = plt.annotate(z_text, xy=(0, 0), xytext=(0.1, 0.9), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	A1_ann = plt.annotate(A1_text, xy=(0, 0), xytext=(0.6, 0.95), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	A2_ann = plt.annotate(A2_text, xy=(0, 0), xytext=(0.6, 0.9), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	A3_ann = plt.annotate(A3_text, xy=(0, 0), xytext=(0.6, 0.85), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	x_list.append(x_ann)
	z_list.append(z_ann)
	A1_list.append(A1_ann)
	A2_list.append(A2_ann)
	A3_list.append(A3_ann)


	return limb1, limb2, limb3, target, button,


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()
