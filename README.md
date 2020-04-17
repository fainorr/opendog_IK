# opendog_IK
During the 2019-2020 school year, the inverse kinematics and navigation sub-team of Lafayette's openDog senior design project worked on developing the **IK motion equations** and **LIDAR analysis techniques** in this repository.

## IK:

1. **ARM_IK_3D.py**: an arm with three links will allow the openDog to interact with its environment.  This python script sets a path for the end-effector, calculates the four joint angles (controlled each by a motor) to achieve that path, and animates the result in 3D space as verification of the equations and requested path.  A visual of the [**arm animation window**](https://github.com/fainorr/opendog_IK/tree/master/images/arm_3d.pdf) defines the links, axes, and angles.

2. **LEG_IK_3D.py**: for openDog locomotion, this script helps develop and visualize various walking gaits in a 3-dimensional animation.  Based on a chosen "action" from the options, it defines the gait parameters and leg phase shifts that accomplish the desired walking pattern, and then employs the three-dimensional inverse kinematic function to solve for the shoulder, femur, and tibia joint angles.  The [**3D walking gait**](https://github.com/fainorr/opendog_IK/tree/master/images/walk_3d.pdf) shows the limb mechanics and prints annotations for the leg in blue.  The angles and geometry are defined in a [**leg diagram**](https://github.com/fainorr/opendog_IK/tree/master/images/leg_model.pdf), where the x-axis points in the forward direction, the y-axis toward the body center, and the z-axis up.

3. **LEG_IK_2D.py**: this python script is a [**2D simplification**](https://github.com/fainorr/opendog_IK/tree/master/images/walk_2d.pdf) of the walking gait, which was used in the first attempts of making openDog walk.

4. **static_gait.py**: the walking tests on the real openDog were unsuccessful at first because the walking gait could not achieve stability; so, a static gait where the legs are moved individually was developed.  This script has a different set of foot position equations, but the IK function and animation are reproduced from the **LEG_IK_3D.py** script.


## LIDAR:

**_visualizing and analyzing scans_**

1. **quad_analysis_methods.py**: to identify obstacles in the environment, three analysis techniques were developed based on raw LIDAR scan data.  For all the techniques, the scan is divided into four quadrants and a certain analysis is performed on each quadrant individually.  This script defines the methods as functions:
    - **"quadrant"**: the boolean output "quad_obstacles" returns 1 if an obstacle (designated by consecutive points) of the specified _obst_size_ exists in the quadrant. The points are only recognized if they exist in a circle of radius _safe_range_.
    - **"percent"**: the output "obst_percent" returns the percentage of points in each quadrant within the _safe_range_.
    - **"intensity"**: the output "obst_intensity" returns a percentage of point intensities in each quadrant.  This point intensity is inversely proportional to the squared distance from the LIDAR.

2. **lidar_animate.py**: using recorded LIDAR scans, the methods were tested and animated.  With a chosen laser scan file _scan_data_ from within the "animate_scans" folder and a selected analysis _method_ from the list of functions, this script animates the data with a [**visual representation**](https://github.com/fainorr/opendog_IK/tree/master/images/lidar_ani.pdf) of how the analysis technique operates.

3. **lidar_compare.py**: using the same analysis techniques developed, this python script compares all three simultaneously for [**single-frame**](https://github.com/fainorr/opendog_IK/tree/master/images/lidar_all.pdf) scans in a greater variety of scenarios.  This helps determine which technique might be most credible in guiding the robot to avoid obstacle collisions.


**_scan text files_**

1. **animate_scans**: for use with **lidar_animate.py**, multiple-frame scans in various locations around Acopian were gathered to better understand how the LIDAR sees its environment.  The title of the **.txt** file indicate where the scan was taken, denoted by a key-word and the nearest room number.

2. **single_frame_scans**: single-frame scans were gathered in more locations around Acopian for visualization in **lidar_compare.py**.
