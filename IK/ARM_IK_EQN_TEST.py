from numpy import *
from math import *

L1 = 16 # inches
L2 = 20 # inches
L3 = 5 # inches

x = 20
z = 15


# inverse kinematics

if (x>0):
    Ad = arctan(z/(x-L3))
else:
    Ad = pi + arctan(z/(x-L3))

d = sqrt((x-L3)**2 + z**2)

A1 = Ad + arccos((L1**2 + d**2 - L2**2)/(2*L1*d))
A2 = arccos((L1**2 + L2**2 - d**2)/(2*L1*L2))
A3 = 2*pi - A1 - A2


# forward kinematics

x_check = L1*cos(A1) + L2*cos(A1+A2-pi) + L3
z_check = L1*sin(A1) + L2*sin(A1+A2-pi)


# LT1 = sqrt((x - L3)**2 + z**2)
# LT2 = sqrt(x**2 + z**2)
#
# AT1 = arccos((L1**2 + LT1**2 - L2**2)/(2*L1*L2))
# AT2 = arcsin(z/LT2)
# AT3 = arccos((x**2 - x*L3 + z**2)/(LT1*LT2))
#
# A1 = AT1 + AT2 + AT3
# A2 = arccos((L1**2 + L2**2 - LT1**2)/(2*L1*L2))
#
# AT5 = pi - AT1 - A2
# AT6 = arcsin(z/LT1)
# AT4 = AT6 - AT5
#
# A3 = pi - AT4

print(A1*180/pi,A2*180/pi,A3*180/pi)
print(x_check,z_check)
