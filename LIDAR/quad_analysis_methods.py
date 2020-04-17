
from numpy import *
from math import *

# ----------------------
# LIDAR ANALYSIS METHODS
# ----------------------
# separate data into four quadrants [left, back, right, front]

# ----------------
# --- QUADRANT ---
# ----------------
# the boolean output "quad_obstacles" returns 1 if an obstacle (designated by
# consecutive points) of the specified obst_size exists in the quadrant. The
# points are only recognized if they exist in a circle of radius safe_range.

def analyze_quadrant(obst_size, in_range):

    quad_obstacles =[0.,0.,0.,0.]

    for quad in range(0,4):
        quad_values = zeros((90-obst_size,1))

        for i in range(90*quad, 90*(quad+1) - obst_size):
            scan_obst_size = 0

            for k in range(0,obst_size):
                if in_range[i+k] == 1: scan_obst_size = scan_obst_size + 1

            if scan_obst_size == obst_size: quad_values[i-90*quad] = 1

        if sum(quad_values >= 1): quad_obstacles[quad] = 1

    return quad_obstacles


# ---------------
# --- PERCENT ---
# ----------------
# the output "obst_percent" returns the percentage of points in each
# quadrant within the safe_range.

def analyze_percent(in_range):

    quad_points = [0.,0.,0.,0.]
    obst_percent = [0.,0.,0.,0.]

    for quad in range(0,4):
        for i in range(90*quad, 90*(quad+1)):
            if in_range[i] == 1: quad_points[quad] = quad_points[quad] + 1

    obst_percent = quad_points/sum(quad_points)*100

    return obst_percent


# -----------------
# --- INTENSITY ---
# -----------------
#  the output "obst_intensity" returns a percentage of point intensities in
# each quadrant. This point intensity is inversely proportional to the squared
# distance from the LIDAR.

def analyze_intensity(distances):

    quad_points = [0.,0.,0.,0.]
    obst_intensity = [0.,0.,0.,0.]

    for quad in range(0,4):
        for i in range(90*quad, 90*(quad+1)):
            if distances[i] != inf:
                quad_points[quad] = quad_points[quad] + distances[i]**2

    for quad in range(0,4):
        if quad_points[quad] > 0:
            obst_intensity[quad] = sum(quad_points)/quad_points[quad]
        else:
            obst_intensity[quad] = inf

    total_obst_intensity = sum(obst_intensity)

    for quad in range(0,4):
        obst_intensity[quad] = obst_intensity[quad]/total_obst_intensity*100

    return obst_intensity
