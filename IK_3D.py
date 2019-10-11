
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FFMpegWriter


# -----------------------
# INVERSE KINEMATICS: 3-D
# -----------------------

# robot dimensions

lf = 2.70 # femur, inches
lt = 2.60 # tibia, inches
ls = 1.40 # shoulder offset, inches

wspine = 2.00 # spine width, inches
lspine = 5.00 # spine, inches


# -------------------------
# establish gait parameters
# -------------------------

gait_duration = 2 # seconds
leg_pace = 25 # pace of gait

x_center = -0.5
x_stride = 1

y_center = -1
y_offset = 0.5

z_center = -3.5
z_lift = 0.5

leg1_offset = 0			# front left
leg2_offset = pi		# front right
leg3_offset = pi		# back left
leg4_offset = 0 		# back right


# initialize: x and z positions for each foot & femur and tibia angles for each leg
# leg indexing: 1-front left, 2-front right, 3-back left, 4-back right

t = linspace(0,gait_duration,1000)

# zeros x, y, z, angs, angf, angt

x1 = zeros(len(t))
y1 = zeros(len(t))
z1 = zeros(len(t))
angs1 = zeros(len(t))
angf1 = zeros(len(t))
angt1 = zeros(len(t))

x2 = zeros(len(t))
y2 = zeros(len(t))
z2 = zeros(len(t))
angs2 = zeros(len(t))
angf2 = zeros(len(t))
angt2 = zeros(len(t))

x3 = zeros(len(t))
y3 = zeros(len(t))
z3 = zeros(len(t))
angs3 = zeros(len(t))
angf3 = zeros(len(t))
angt3 = zeros(len(t))

x4 = zeros(len(t))
y4 = zeros(len(t))
z4 = zeros(len(t))
angs4 = zeros(len(t))
angf4 = zeros(len(t))
angt4 = zeros(len(t))


# develop functions for foot positions for given gait

for i in range(0,len(t)):
	x1[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg1_offset)
	y1[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg1_offset)
	z1[i] = z_center + z_lift*sin(leg_pace*t[i] - leg1_offset)

	x2[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg2_offset)
	y2[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg2_offset)
	z2[i] = z_center + z_lift*sin(leg_pace*t[i] - leg2_offset)

	x3[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg3_offset)
	y3[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg3_offset)
	z3[i] = z_center + z_lift*sin(leg_pace*t[i] - leg3_offset)

	x4[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg4_offset)
	y4[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg4_offset)
	z4[i] = z_center + z_lift*sin(leg_pace*t[i] - leg4_offset)


# ---------------------------
# INVERSE KINEMATICS FUNCTION
# ---------------------------

#  to solve for servo angles As (shoulder), Af (femur), and At (tibia)

def getServoAng(x, y, z, ls, lf, lt, leg):

# by geometry
	if (y<0):
		Adxy = arctan(z/y)
	else:
		Adxy = pi + arctan(z/y)

	dxy = sqrt(y**2 + z**2)
	As = Adxy - arccos(ls/dxy)

	if (leg == 1 or leg == 3):
		As = pi-As

		if (x<0):
			Ad = pi + arctan((z+ls*sin(As))/x)
		else:
			Ad = arctan((z+ls*sin(As))/x)

		d = sqrt(x**2 + (z+ls*sin(As))**2)
		Af = Ad - arccos((lf**2 + d**2 - lt**2)/(2*lf*d))
		At = pi - arccos((lf**2 + lt**2 - d**2)/(2*lf*lt))

		Af = pi-Af
		At = -At

	else:
		if (x<0):
			Ad = arctan((z+ls*sin(As))/x)
		else:
			Ad = pi + arctan((z+ls*sin(As))/x)

		d = sqrt(x**2 + (z+ls*sin(As))**2)
		Af = Ad - arccos((lf**2 + d**2 - lt**2)/(2*lf*d))
		At = pi - arccos((lf**2 + lt**2 - d**2)/(2*lf*lt))


	return As,Af,At


# ----------------
# ANIMATION FIGURE
# ----------------

figxz = plt.figure()
plt.axis('equal')
figxz.patch.set_facecolor('w')
ax1 = plt.axes(xlim=(-(lf+lt)-lspine,(lf+lt)), ylim=(-(lf+lt),(lf+lt)))
figxz.suptitle('Side View x,z', fontsize=16)

figxy = plt.figure()
plt.axis('equal')
figxy.patch.set_facecolor('w')
ax2 = plt.axes(xlim=(-(lf+lt)-lspine,(lf+lt)), ylim=(-(lf+lt),(lf+lt)))
figxy.suptitle('Top View x,y', fontsize=16)

figyz = plt.figure()
plt.axis('equal')
figyz.patch.set_facecolor('w')
ax3 = plt.axes(xlim=(-(lf+lt)-lspine,(lf+lt)), ylim=(-(lf+lt),(lf+lt)))
figyz.suptitle('Front View y,z', fontsize=16)


# initialize elements in plots

slinexz3, = ax1.plot([],[],lw=5,c='0.7')
flinexz3, = ax1.plot([],[],lw=5,c='0.7')
tlinexz3, = ax1.plot([],[],lw=5,c='0.7')
targetxz3, = ax1.plot([],[],lw=5,c='0.7')

targetxy3, = ax2.plot([],[],lw=5,c='0.7')
tlinexy3, = ax2.plot([],[],lw=5,c='0.7')
flinexy3, = ax2.plot([],[],lw=5,c='0.4')
slinexy3, = ax2.plot([],[],lw=5,c='0.4')

slineyz3, = ax3.plot([],[],lw=5,c='0.7')
flineyz3, = ax3.plot([],[],lw=5,c='0.7')
tlineyz3, = ax3.plot([],[],lw=5,c='0.7')
targetyz3, = ax3.plot([],[],lw=5,c='0.7')


slinexz1, = ax1.plot([],[],lw=5,c='0.7')
flinexz1, = ax1.plot([],[],lw=5,c='0.7')
tlinexz1, = ax1.plot([],[],lw=5,c='0.7')
targetxz1, = ax1.plot([],[],lw=5,c='0.7')

targetxy1, = ax2.plot([],[],lw=5,c='0.4')
tlinexy1, = ax2.plot([],[],lw=5,c='0.7')
flinexy1, = ax2.plot([],[],lw=5,c='0.4')
slinexy1, = ax2.plot([],[],lw=5,c='0.4')

slineyz1, = ax3.plot([],[],lw=5,c='0.4')
flineyz1, = ax3.plot([],[],lw=5,c='0.4')
tlineyz1, = ax3.plot([],[],lw=5,c='0.4')
targetyz1, = ax3.plot([],[],lw=5,c='0.4')


spinexz, = ax1.plot([],[],lw=8,c='0.5')
spinexy, = ax2.plot([],[],lw=8,c='0.5')
spineyz, = ax3.plot([],[],lw=8,c='0.5')


slinexz4, = ax1.plot([],[],lw=5,c='0.4')
flinexz4, = ax1.plot([],[],lw=5,c='0.4')
tlinexz4, = ax1.plot([],[],lw=5,c='0.4')
targetxz4, = ax1.plot([],[],lw=5,c='0.4')

targetxy4, = ax2.plot([],[],lw=5,c='0.7')
tlinexy4, = ax2.plot([],[],lw=5,c='0.7')
flinexy4, = ax2.plot([],[],lw=5,c='0.4')
slinexy4, = ax2.plot([],[],lw=5,c='0.4')

slineyz4, = ax3.plot([],[],lw=5,c='0.7')
flineyz4, = ax3.plot([],[],lw=5,c='0.7')
tlineyz4, = ax3.plot([],[],lw=5,c='0.7')
targetyz4, = ax3.plot([],[],lw=5,c='0.7')


slinexz2, = ax1.plot([],[],lw=5,c='0.4')
flinexz2, = ax1.plot([],[],lw=5,c='0.4')
tlinexz2, = ax1.plot([],[],lw=5,c='0.4')
targetxz2, = ax1.plot([],[],lw=5,c='b')

tlinexy2, = ax2.plot([],[],lw=5,c='0.7')
targetxy2, = ax2.plot([],[],lw=5,c='b')
flinexy2, = ax2.plot([],[],lw=5,c='0.4')
slinexy2, = ax2.plot([],[],lw=5,c='0.4')

slineyz2, = ax3.plot([],[],lw=5,c='0.4')
flineyz2, = ax3.plot([],[],lw=5,c='0.4')
tlineyz2, = ax3.plot([],[],lw=5,c='0.4')
targetyz2, = ax3.plot([],[],lw=5,c='b')

x_ann_list = []
y_ann_list = []
z_ann_list = []
As_ann_list = []
Af_ann_list = []
At_ann_list = []

ax1.legend([flinexy1, flinexy2], ['left legs', 'right legs'], loc='west')


def init():

	# spine.set_data([],[])

	spinexz.set_data([],[])
	spinexy.set_data([],[])
	spineyz.set_data([],[])

	slinexz1.set_data([],[])
	flinexz1.set_data([],[])
	tlinexz1.set_data([],[])
	targetxz1.set_data([],[])

	slinexy1.set_data([],[])
	flinexy1.set_data([],[])
	tlinexy1.set_data([],[])
	targetxy1.set_data([],[])

	slineyz1.set_data([],[])
	flineyz1.set_data([],[])
	tlineyz1.set_data([],[])
	targetyz1.set_data([],[])

	slinexz2.set_data([],[])
	flinexz2.set_data([],[])
	tlinexz2.set_data([],[])
	targetxz2.set_data([],[])

	slinexy2.set_data([],[])
	flinexy2.set_data([],[])
	tlinexy2.set_data([],[])
	targetxy2.set_data([],[])

	slineyz2.set_data([],[])
	flineyz2.set_data([],[])
	tlineyz2.set_data([],[])
	targetyz2.set_data([],[])

	slinexz3.set_data([],[])
	flinexz3.set_data([],[])
	tlinexz3.set_data([],[])
	targetxz3.set_data([],[])

	slinexy3.set_data([],[])
	flinexy3.set_data([],[])
	tlinexy3.set_data([],[])
	targetxy3.set_data([],[])

	slineyz3.set_data([],[])
	flineyz3.set_data([],[])
	tlineyz3.set_data([],[])
	targetyz3.set_data([],[])

	slinexz4.set_data([],[])
	flinexz4.set_data([],[])
	tlinexz4.set_data([],[])
	targetxz4.set_data([],[])

	slinexy4.set_data([],[])
	flinexy4.set_data([],[])
	tlinexy4.set_data([],[])
	targetxy4.set_data([],[])

	slineyz4.set_data([],[])
	flineyz4.set_data([],[])
	tlineyz4.set_data([],[])
	targetyz4.set_data([],[])

	return slinexz1, flinexz1, tlinexz1, targetxz1, \
			slinexy1, flinexy1, tlinexy1, targetxy1, \
			slineyz1, flineyz1, tlineyz1, targetyz1, \
			slinexz2, flinexz2, tlinexz2, targetxz2, \
			slinexy2, flinexy2, tlinexy2, targetxy2, \
			slineyz2, flineyz2, tlineyz2, targetyz2, \
			spinexz, spinexy, spineyz, \
			slinexz3, flinexz3, tlinexz3, targetxz3, \
			slinexy3, flinexy3, tlinexy3, targetxy3, \
			slineyz3, flineyz3, tlineyz3, targetyz3, \
			slinexz4, flinexz4, tlinexz4, targetxz4, \
			slinexy4, flinexy4, tlinexy4, targetxy4, \
			slineyz4, flineyz4, tlineyz4, targetyz4


def animate(i):

	# solve for angles for each leg

	angs1[i], angf1[i], angt1[i] = getServoAng(x1[i], y1[i], z1[i], ls, lf, lt, 1)
	angs2[i], angf2[i], angt2[i] = getServoAng(x2[i], y2[i], z2[i], ls, lf, lt, 2)
	angs3[i], angf3[i], angt3[i] = getServoAng(x3[i], y3[i], z3[i], ls, lf, lt, 3)
	angs4[i], angf4[i], angt4[i] = getServoAng(x4[i], y4[i], z4[i], ls, lf, lt, 4)


	# ----------------------------
	# FORWARD KINEMATICS EQUATIONS
	# ----------------------------

	# given these angles, solve for the limb positions for simulation

	xs1 = [0, 0]
	ys1 = [wspine, wspine-ls*cos(angs1[i])]
	zs1 = [0, -ls*sin(angs1[i])]

	xf1 = [xs1[1], xs1[1] - lf*cos(angf1[i])]
	yf1 = [ys1[1], ys1[1] + lf*sin(angf1[i])*sin(angs1[i])]
	zf1 = [zs1[1], zs1[1] - lf*sin(angf1[i])*cos(angs1[i])]

	xt1 = [xf1[1], xf1[1] - lt*cos(angt1[i] + angf1[i])]
	yt1 = [yf1[1], yf1[1] + lt*sin(angt1[i] + angf1[i])*sin(angs1[i])]
	zt1 = [zf1[1], zf1[1] - lt*sin(angt1[i] + angf1[i])*cos(angs1[i])]

	xtg1 = [x1[i], x1[i]]
	ytg1 = [wspine-y1[i], wspine-y1[i]]
	ztg1 = [z1[i], z1[i]]


	xs2 = [0, 0]
	ys2 = [0, -ls*cos(angs2[i])]
	zs2 = [0, -ls*sin(angs2[i])]

	xf2 = [xs2[1], xs2[1] - lf*cos(angf2[i])]
	yf2 = [ys2[1], ys2[1] + lf*sin(angf2[i])*sin(angs2[i])]
	zf2 = [zs2[1], zs2[1] - lf*sin(angf2[i])*cos(angs2[i])]

	xt2 = [xf2[1], xf2[1] - lt*cos(angt2[i] + angf2[i])]
	yt2 = [yf2[1], yf2[1] + lt*sin(angt2[i] + angf2[i])*sin(angs2[i])]
	zt2 = [zf2[1], zf2[1] - lt*sin(angt2[i] + angf2[i])*cos(angs2[i])]

	xtg2 = [x2[i], x2[i]]
	ytg2 = [y2[i], y2[i]]
	ztg2 = [z2[i], z2[i]]


	xs3 = [-lspine, -lspine]
	ys3 = [wspine, wspine-ls*cos(angs3[i])]
	zs3 = [0, -ls*sin(angs3[i])]

	xf3 = [xs3[1], xs3[1] - lf*cos(angf3[i])]
	yf3 = [ys3[1], ys3[1] + lf*sin(angf3[i])*sin(angs3[i])]
	zf3 = [zs3[1], zs3[1] - lf*sin(angf3[i])*cos(angs3[i])]

	xt3 = [xf3[1], xf3[1] - lt*cos(angt3[i] + angf3[i])]
	yt3 = [yf3[1], yf3[1] + lt*sin(angt3[i] + angf3[i])*sin(angs3[i])]
	zt3 = [zf3[1], zf3[1] - lt*sin(angt3[i] + angf3[i])*cos(angs3[i])]

	xtg3 = [x3[i]-lspine, x3[i]-lspine]
	ytg3 = [wspine-y3[i], wspine-y3[i]]
	ztg3 = [z3[i], z3[i]]


	xs4 = [-lspine, -lspine]
	ys4 = [0, -ls*cos(angs4[i])]
	zs4 = [0, -ls*sin(angs4[i])]

	xf4 = [xs4[1], xs4[1] - lf*cos(angf4[i])]
	yf4 = [ys4[1], ys4[1] + lf*sin(angf4[i])*sin(angs4[i])]
	zf4 = [zs4[1], zs4[1] - lf*sin(angf4[i])*cos(angs4[i])]

	xt4 = [xf4[1], xf4[1] - lt*cos(angt4[i] + angf4[i])]
	yt4 = [yf4[1], yf4[1] + lt*sin(angt4[i] + angf4[i])*sin(angs4[i])]
	zt4 = [zf4[1], zf4[1] - lt*sin(angt4[i] + angf4[i])*cos(angs4[i])]

	xtg4 = [x4[i]-lspine, x4[i]-lspine]
	ytg4 = [y4[i], y4[i]]
	ztg4 = [z4[i], z4[i]]


	# write calculated position to limb elements in figure

	slinexz1.set_data(xs1, zs1)
	flinexz1.set_data(xf1, zf1)
	tlinexz1.set_data(xt1, zt1)
	targetxz1.set_data(xtg1, ztg1)

	slinexy1.set_data(xs1, ys1)
	flinexy1.set_data(xf1, yf1)
	tlinexy1.set_data(xt1, yt1)
	targetxy1.set_data(xtg1, ytg1)

	slineyz1.set_data(ys1, zs1)
	flineyz1.set_data(yf1, zf1)
	tlineyz1.set_data(yt1, zt1)
	targetyz1.set_data(ytg1, ztg1)

	slinexz2.set_data(xs2, zs2)
	flinexz2.set_data(xf2, zf2)
	tlinexz2.set_data(xt2, zt2)
	targetxz2.set_data(xtg2, ztg2)

	slinexy2.set_data(xs2, ys2)
	flinexy2.set_data(xf2, yf2)
	tlinexy2.set_data(xt2, yt2)
	targetxy2.set_data(xtg2, ytg2)

	slineyz2.set_data(ys2, zs2)
	flineyz2.set_data(yf2, zf2)
	tlineyz2.set_data(yt2, zt2)
	targetyz2.set_data(ytg2, ztg2)

	slinexz3.set_data(xs3, zs3)
	flinexz3.set_data(xf3, zf3)
	tlinexz3.set_data(xt3, zt3)
	targetxz3.set_data(xtg3, ztg3)

	slinexy3.set_data(xs3, ys3)
	flinexy3.set_data(xf3, yf3)
	tlinexy3.set_data(xt3, yt3)
	targetxy3.set_data(xtg3, ytg3)

	slineyz3.set_data(ys3, zs3)
	flineyz3.set_data(yf3, zf3)
	tlineyz3.set_data(yt3, zt3)
	targetyz3.set_data(ytg3, ztg3)

	slinexz4.set_data(xs4, zs4)
	flinexz4.set_data(xf4, zf4)
	tlinexz4.set_data(xt4, zt4)
	targetxz4.set_data(xtg4, ztg4)

	slinexy4.set_data(xs4, ys4)
	flinexy4.set_data(xf4, yf4)
	tlinexy4.set_data(xt4, yt4)
	targetxy4.set_data(xtg4, ytg4)

	slineyz4.set_data(ys4, zs4)
	flineyz4.set_data(yf4, zf4)
	tlineyz4.set_data(yt4, zt4)
	targetyz4.set_data(ytg4, ztg4)

	spinexz.set_data([-lspine,0],[0,0])
	spinexy.set_data([-lspine,0],[wspine/2,wspine/2])
	spineyz.set_data([0,wspine],[0,0])


	# create annotations with live updates about foot position and joint angles (for leg 1)

	x_text = "target x: {:.1f}".format(xtg2[0])
	y_text = "target y: {:.1f}".format(ytg2[0])
	z_text = "target z: {:.1f}".format(ztg2[0])
	As_text = "shoulder angle: {:.0f}".format(angs2[i]*180/pi)
	Af_text = "femur angle: {:.0f}".format(angf2[i]*180/pi)
	At_text = "tibia angle: {:.0f}".format(angt2[i]*180/pi)


	# remove previous annotations

	for j, a in enumerate(x_ann_list):
		a.remove()
	for j, a in enumerate(y_ann_list):
		a.remove()
	for j, a in enumerate(z_ann_list):
		a.remove()
	for j, a in enumerate(As_ann_list):
		a.remove()
	for j, a in enumerate(Af_ann_list):
		a.remove()
	for j, a in enumerate(At_ann_list):
		a.remove()

	x_ann_list[:] = []
	y_ann_list[:] = []
	z_ann_list[:] = []
	As_ann_list[:] = []
	Af_ann_list[:] = []
	At_ann_list[:] = []


	# apply annotations to figure

	x_ann = plt.annotate(x_text, xy=(0, 0), xytext=(0.1, 0.95), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	y_ann = plt.annotate(y_text, xy=(0, 0), xytext=(0.1, 0.9), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	z_ann = plt.annotate(z_text, xy=(0, 0), xytext=(0.1, 0.85), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	As_ann = plt.annotate(As_text, xy=(0, 0), xytext=(0.1, 0.75), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	Af_ann = plt.annotate(Af_text, xy=(0, 0), xytext=(0.1, 0.7), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	At_ann = plt.annotate(At_text, xy=(0, 0), xytext=(0.1, 0.65), textcoords='axes fraction',
            horizontalalignment='left', verticalalignment='top')

	x_ann_list.append(x_ann)
	y_ann_list.append(y_ann)
	z_ann_list.append(z_ann)
	As_ann_list.append(As_ann)
	Af_ann_list.append(Af_ann)
	At_ann_list.append(At_ann)


 	return slinexz1, flinexz1, tlinexz1, targetxz1, \
			slinexy1, flinexy1, tlinexy1, targetxy1, \
			slineyz1, flineyz1, tlineyz1, targetyz1, \
			slinexz2, flinexz2, tlinexz2, targetxz2, \
			slinexy2, flinexy2, tlinexy2, targetxy2, \
			slineyz2, flineyz2, tlineyz2, targetyz2, \
			spinexz, spinexy, spineyz, \
			slinexz3, flinexz3, tlinexz3, targetxz3, \
			slinexy3, flinexy3, tlinexy3, targetxy3, \
			slineyz3, flineyz3, tlineyz3, targetyz3, \
			slinexz4, flinexz4, tlinexz4, targetxz4, \
			slinexy4, flinexy4, tlinexy4, targetxy4, \
			slineyz4, flineyz4, tlineyz4, targetyz4,


anixz = animation.FuncAnimation(figxz, animate, init_func=init, frames = len(t), interval = 20, blit=False)

anixy = animation.FuncAnimation(figxy, animate, init_func=init, frames = len(t), interval = 20, blit=False)

aniyz = animation.FuncAnimation(figyz, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()





