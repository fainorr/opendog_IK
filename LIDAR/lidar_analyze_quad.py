
# breaks scan into four quadrants
# checks for obst_size (number of consecutive dots) within safe_range
# passes array of booleans (true is obstacle exists) [front, left, right, back]

from numpy import *
from math import *
import time
from matplotlib import pyplot as plt

# call specific laser scan file
scan_data = 'LIDAR/lidar_sample_scan.txt'


# process scan data

angles = arange(-pi, pi, pi/180)


distances = zeros(len(angles))
with open(scan_data) as f:
    distances = f.read().split(', ')

for i in range(0,len(angles)):
    distances[i] = round(float(distances[i]),5)

# analyze scan data

obst_size = 4;         # number of consecutive dots
safe_range = 0.5;      # search ranges for obstacles

quad_obstacles = [0,0,0,0]

print(distances)

for i in range(0,360):
    if distances[i] > safe_range: distances[i] = 0
    else: distances[i] = 1

print(distances)

for quad in range(0,4):
    quad_check = zeros((90-obst_size,1))

    for j in range(90*quad, 90*(quad+1) - obst_size):
        print(j)
        print(quad)
        scan_obst_size = 0

        for k in range(0,obst_size):
            if distances[j+k] == 1: scan_obst_size = scan_obst_size + 1

        # print(scan_obst_size)
        if scan_obst_size == obst_size: quad_check[j-90*quad] = 1

    if sum(quad_check >= 1): quad_obstacles[quad] = 1

print(quad_check)
print(quad_obstacles)
