
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
# import ffmpeg as ffmpeg


# Inverse Kinematics: 2-D

# leg dimensions

lf = 2.70 # inches
lt = 2.60 # inches

gait_duration = 2 # seconds

t = linspace(0,gait_duration,1000)

x1 = zeros(len(t))
z1 = zeros(len(t))
angf = zeros(len(t))
angt = zeros(len(t))


# servo angles Af (femur) and At (tibia)

def getServoAng(x1,z1,lf,lt):
	if (x1<0):
		Ad = arctan(z1/x1)
	else:
		Ad = pi + arctan(z1/x1)

	d = sqrt(x1**2+z1**2)

	Af = Ad - arccos((lf**2 + d**2 - lt**2)/(2*lf*d))
	At = pi - arccos((lf**2 + lt**2 - d**2)/(2*lf*lt))

	return Af,At

for i in range(0,len(z1)):
	x1[i] = -0.5 + sin(10*t[i]+pi/2)
	z1[i] = -3 - 0.5*sin(10*t[i])

	angf[i], angt[i] = getServoAng(x1[i],z1[i],lf,lt)


# create animation figure

fig = plt.figure()
plt.axis('equal')
ax = plt.axes(xlim=(-(lf+lt),(lf+lt)), ylim=(-(lf+lt),(lf+lt)))
fline, = ax.plot([],[],lw=5)
tline, = ax.plot([],[],lw=5)
target, = ax.plot([],[],lw=5)

x_ann_list = []
z_ann_list = []
Af_ann_list = []
At_ann_list = []


def init():
	fline.set_data([],[])
	tline.set_data([],[])
	target.set_data([],[])
	return fline, tline, target,

def animate(i):

	angf,angt = getServoAng(x1[i],z1[i],lf,lt)
	xf = [0,-lf*cos(angf)]
	zf = [0,-lf*sin(angf)]

	xt = [xf[1],xf[1]-lt*cos(angt+angf)]
	zt = [zf[1],zf[1]-lt*sin(angt+angf)]

	xtg = [x1[i], x1[i]]
	ztg = [z1[i], z1[i]]

	#print angf*180/pi, angt*180/pi

	fline.set_data(xf,zf)
	tline.set_data(xt,zt)
	target.set_data(xtg,ztg)

	x_text = "target x: {:.1f}".format(xtg[0])
	z_text = "target z: {:.1f}".format(ztg[0])
	Af_text = "femur angle: {:.0f}".format(angf*180/pi)
	At_text = "tibia angle: {:.0f}".format(angt*180/pi)

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

	x_ann = plt.annotate(x_text, xy=(0, 0), xytext=(0.7, 0.95), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	z_ann = plt.annotate(z_text, xy=(0, 0), xytext=(0.7, 0.9), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	Af_ann = plt.annotate(Af_text, xy=(0, 0), xytext=(0.7, 0.8), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	At_ann = plt.annotate(At_text, xy=(0, 0), xytext=(0.7, 0.75), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	x_ann_list.append(x_ann)
	z_ann_list.append(z_ann)
	Af_ann_list.append(Af_ann)
	At_ann_list.append(At_ann)


 	return fline, tline, target,


ani = animation.FuncAnimation(fig, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()

