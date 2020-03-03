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

gait_duration = 2 # seconds
x_start = 10
x_final = 20
x_pace = 25
z_final = 15

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
