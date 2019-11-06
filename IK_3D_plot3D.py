
from numpy import *
from math import *
import time
from matplotlib import pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
from mpl_toolkits import mplot3d


# -----------------------
# INVERSE KINEMATICS: 3-D
# -----------------------

# robot dimensions

lf = 2.70 # femur, inches
lt = 2.60 # tibia, inches
ls = 1.40 # shoulder offset, inches

wspine = 2.00 # spine width, inches
lspine = 5.00 # spine, inches


# ACTION CHOICES: forward, turn, swivel, sideways

action = "turn"

# -------------------------
# establish gait parameters
# -------------------------

gait_duration = 2 # seconds
leg_pace = 80 # pace of gait

if (action == "forward"):
	x_center = 0.5
	x_stride = 1

	y_center = -1
	y_offset = 0.5

	z_center = -4
	z_lift = 1

	leg1_offset = 0			# front left
	leg2_offset = pi		# front right
	leg3_offset = pi		# back left
	leg4_offset = 0 		# back right

elif (action == "turn"):
	x_center = 1
	x_stride = 0

	y_center = 0
	y_offset = 0.5

	z_center = -4.5
	z_lift = 1.5

	leg1_offset = 0			# front left
	leg2_offset = pi		# front right
	leg3_offset = pi		# back left
	leg4_offset = 0 		# back right

elif (action == "swivel"):
	x_center = 0.5
	x_stride = 1

	y_center = -0.5
	y_offset = 1

	z_center = -4
	z_lift = 0

	leg1_offset = 0			# front left
	leg2_offset = 0			# front right
	leg3_offset = 0			# back left
	leg4_offset = 0 		# back right

elif (action == "sideways"):
	x_center = 0
	x_stride = 0

	y_center = -1
	y_offset = 0.5

	z_center = -4
	z_lift = 1

	leg1_offset = 0			# front left
	leg2_offset = pi		# front right
	leg3_offset = 0			# back left
	leg4_offset = pi 		# back right


# initialize: x, y, and z positions for each foot & femur and tibia angles for each leg
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
	
	if (action == "forward"):
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

		if (z1[i]) < z_center: z1[i] = z_center
		if (z2[i]) < z_center: z2[i] = z_center
		if (z3[i]) < z_center: z3[i] = z_center
		if (z4[i]) < z_center: z4[i] = z_center

	elif (action == "turn"):
		x1[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg1_offset)
		y1[i] = y_center - y_offset*sin(leg_pace*t[i] - pi - leg1_offset)
		z1[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg1_offset)

		x2[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg2_offset)
		y2[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg2_offset)
		z2[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg2_offset)

		x3[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg3_offset)
		y3[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg3_offset)
		z3[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg3_offset)

		x4[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg4_offset)
		y4[i] = y_center - y_offset*sin(leg_pace*t[i] - pi - leg4_offset)
		z4[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg4_offset)

		if (z1[i]) < z_center: z1[i] = z_center
		if (z2[i]) < z_center: z2[i] = z_center
		if (z3[i]) < z_center: z3[i] = z_center
		if (z4[i]) < z_center: z4[i] = z_center

	elif (action == "swivel"):
		x1[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg1_offset)
		y1[i] = y_center - y_offset*sin(leg_pace*t[i] - pi - leg1_offset)
		z1[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg1_offset)

		x2[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg2_offset)
		y2[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg2_offset)
		z2[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg2_offset)

		x3[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg3_offset)
		y3[i] = y_center + y_offset*sin(leg_pace*t[i] - leg3_offset)
		z3[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg3_offset)

		x4[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 -leg4_offset)
		y4[i] = y_center - y_offset*sin(leg_pace*t[i] - leg4_offset)
		z4[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg4_offset)

		if (z1[i]) < z_center: z1[i] = z_center
		if (z2[i]) < z_center: z2[i] = z_center
		if (z3[i]) < z_center: z3[i] = z_center
		if (z4[i]) < z_center: z4[i] = z_center

	elif (action == "sideways"):
		x1[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg1_offset)
		y1[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg1_offset)
		z1[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg1_offset)

		x2[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg2_offset)
		y2[i] = y_center - y_offset*sin(leg_pace*t[i] - pi - leg2_offset)
		z2[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg2_offset)

		x3[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg3_offset)
		y3[i] = y_center + y_offset*sin(leg_pace*t[i] - pi - leg3_offset)
		z3[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg3_offset)

		x4[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - leg4_offset)
		y4[i] = y_center - y_offset*sin(leg_pace*t[i] - pi - leg4_offset)
		z4[i] = z_center + z_lift*sin(leg_pace*t[i] - pi/2 - leg4_offset)

		if (z1[i]) < z_center: z1[i] = z_center
		if (z2[i]) < z_center: z2[i] = z_center
		if (z3[i]) < z_center: z3[i] = z_center
		if (z4[i]) < z_center: z4[i] = z_center


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

figxyz = plt.figure()
figxyz.patch.set_facecolor('w')
ax1 = plt.axes(projection='3d') #, xlim=(-(lf+lt)-lspine,(lf+lt)), ylim=(-(lf+lt),(lf+lt)), zlim=(-(lf+lt),(lf+lt)))
ax1.set_xlim(-8,2)
ax1.set_ylim(-4,6)
ax1.set_zlim(-6,4)


# initialize elements in plots

sline3, = ax1.plot([],[],[],lw=5,c='0.7')
fline3, = ax1.plot([],[],[],lw=5,c='0.7')
tline3, = ax1.plot([],[],[],lw=5,c='0.7')
target3, = ax1.plot([],[],[],lw=5,c='0.7')

sline1, = ax1.plot([],[],[],lw=5,c='0.7')
fline1, = ax1.plot([],[],[],lw=5,c='0.7')
tline1, = ax1.plot([],[],[],lw=5,c='0.7')
target1, = ax1.plot([],[],[],lw=5,c='0.7')

spine, = ax1.plot([],[],[],lw=20,c='0.5')

sline4, = ax1.plot([],[],[],lw=5,c='0.4')
fline4, = ax1.plot([],[],[],lw=5,c='0.4')
tline4, = ax1.plot([],[],[],lw=5,c='0.4')
target4, = ax1.plot([],[],[],lw=5,c='0.4')

sline2, = ax1.plot([],[],[],lw=5,c='b')
fline2, = ax1.plot([],[],[],lw=5,c='b')
tline2, = ax1.plot([],[],[],lw=5,c='b')
target2, = ax1.plot([],[],[],lw=5,c='b')

x_ann_list = []
y_ann_list = []
z_ann_list = []
As_ann_list = []
Af_ann_list = []
At_ann_list = []

#ax1.legend([fline1, fline2], ['left legs', 'right legs'], loc='west')


def init():

	spine.set_data([],[])
	spine.set_3d_properties([])

	sline1.set_data([],[])
	fline1.set_data([],[])
	tline1.set_data([],[])
	target1.set_data([],[])
	sline1.set_3d_properties([])
	fline1.set_3d_properties([])
	tline1.set_3d_properties([])
	target1.set_3d_properties([])

	sline2.set_data([],[])
	fline2.set_data([],[])
	tline2.set_data([],[])
	target2.set_data([],[])
	sline2.set_3d_properties([])
	fline2.set_3d_properties([])
	tline2.set_3d_properties([])
	target2.set_3d_properties([])

	sline3.set_data([],[])
	fline3.set_data([],[])
	tline3.set_data([],[])
	target3.set_data([],[])
	sline3.set_3d_properties([])
	fline3.set_3d_properties([])
	tline3.set_3d_properties([])
	target3.set_3d_properties([])

	sline4.set_data([],[])
	fline4.set_data([],[])
	tline4.set_data([],[])
	target4.set_data([],[])
	sline4.set_3d_properties([])
	fline4.set_3d_properties([])
	tline4.set_3d_properties([])
	target4.set_3d_properties([])

	return sline1, fline1, tline1, target1, sline2, fline2, tline2, target2, \
			spine, sline3, fline3, tline3, target3, sline4, fline4, tline4, target4


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

	sline1.set_data(xs1, ys1)
	fline1.set_data(xf1, yf1)
	tline1.set_data(xt1, yt1)
	target1.set_data(xtg1, ytg1)
	sline1.set_3d_properties(zs1)
	fline1.set_3d_properties(zf1)
	tline1.set_3d_properties(zt1)
	target1.set_3d_properties(ztg1)

	sline2.set_data(xs2, ys2)
	fline2.set_data(xf2, yf2)
	tline2.set_data(xt2, yt2)
	target2.set_data(xtg2, ytg2)
	sline2.set_3d_properties(zs2)
	fline2.set_3d_properties(zf2)
	tline2.set_3d_properties(zt2)
	target2.set_3d_properties(ztg2)

	sline3.set_data(xs3, ys3)
	fline3.set_data(xf3, yf3)
	tline3.set_data(xt3, yt3)
	target3.set_data(xtg3, ytg3)
	sline3.set_3d_properties(zs3)
	fline3.set_3d_properties(zf3)
	tline3.set_3d_properties(zt3)
	target3.set_3d_properties(ztg3)

	sline4.set_data(xs4, ys4)
	fline4.set_data(xf4, yf4)
	tline4.set_data(xt4, yt4)
	target4.set_data(xtg4, ytg4)
	sline4.set_3d_properties(zs4)
	fline4.set_3d_properties(zf4)
	tline4.set_3d_properties(zt4)
	target4.set_3d_properties(ztg4)

	spine.set_data([-lspine,0],[wspine/2,wspine/2])
	spine.set_3d_properties([0,0])



	# create annotations with live updates about foot position and joint angles (for leg 1)

	x_text = "target x: {:.1f}".format(xtg1[0])
	y_text = "target y: {:.1f}".format(ytg1[0])
	z_text = "target z: {:.1f}".format(ztg1[0])
	As_text = "shoulder angle: {:.0f}".format(angs1[i]*180/pi)
	Af_text = "femur angle: {:.0f}".format(angf1[i]*180/pi)
	At_text = "tibia angle: {:.0f}".format(angt1[i]*180/pi)


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


 	return sline1, fline1, tline1, target1, sline2, fline2, tline2, target2, \
			spine, sline3, fline3, tline3, target3, sline4, fline4, tline4, target4,


ani = animation.FuncAnimation(figxyz, animate, init_func=init, frames = len(t), interval = 20, blit=False)
plt.show()




