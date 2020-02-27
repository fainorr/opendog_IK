from numpy import *
from math import *
import time
from matplotlib import pyplot as plt 
from matplotlib import animation
from matplotlib.animation import FFMpegWriter


# ARM INVERSE KINEMATICS 2-D

# arm dimensions

L1 = 16 # piece connected to base, inches
L2 = 20 # middle piece, inches
L3 = 5 # end/tip, inches


# establish parameters

duration = 2 # seconds
pace = 25 # pace of movement

x_center = 0
x_stride = 0.5

z_center = -3
z_lift = 0.5

offset = 0

t = linspace(0,duration,1000)

x = zeros(len(t))
z = zeros(len(t))
ang1 = zeros(len(t))
ang2 = zeros(len(t))
ang3 = zeros(len(t))


for i in range(0,len(t)):
	x[i] = x_center + x_stride*sin(leg_pace*t[i] - pi/2 - offset)
	z[i] = z_center + z_lift*sin(leg_pace*t[i] - offset)

def getServoAng(x, z, L1, L2, L3):

	LT1 = sqrt((x - L3)**2 + z**2)
	LT2 = sqrt(x**2 + z**2)

	AT1 = arccos((L1**2 + LT1**2 - L2**2)/(2*L1*L2))
	AT2 = arcsin(z/LT2)
	AT3 = arccos((x**2 - x*L3 + z**2)/(LT1*LT2))

	A1 = AT1 + AT2 + AT3
	A2 = arccos((L1**2 + L2**2 - LT1**2)/(2*L1*L2))

	AT5 = 180 - AT1 - A2
	AT6 = arcsin(z/LT1)
	AT4 = AT6 - AT5

	A3 = 180 - AT4

	return A1,A2,A3

# ANIMATION FIGURE

#fig = plt.figure()
#plt.axis('equal')
#fig.patch.set_facecolor('w')
#ax = plt.axez(xlin=(-(L1+L2+L3),(L1+L2+L3)), ylim=(-(L1+L2+L3),(L1+L2+L3)))

#line1, = ax.plot([],[],lw=5,c='0.7')
#line2, = ax.plot([],[],lw=5,c='0.7')
#line3, = ax.plot([],[],lw=5,c='0.7')
#target, = ax.plot([],[],lw=5,c='b')

#x_ann_list = []
#z_ann_list = []
#A1_ann_list = []
#A2_ann_list = []
#A3_ann_list = []

#ax.legend([line1, line2, line3], ['bottom link', 'middle link', 'pointer'], loc='west')


#def init():

#	line1.set_data([],[])
#	line2.set_data([],[])
#	line3.set_data([],[])
#	target.set_dta([],[])

#	return line1, line2, line3, target