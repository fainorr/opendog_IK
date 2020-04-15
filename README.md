# opendog_IK
During the 2019-2020 school year, the inverse kinematics and navigation sub-team of Lafayette's openDog senior design project worked on developing the **IK motion equations** and **LIDAR analysis techniques** in this repository.

### IK:

1. **ARM_IK_3D.py**: an arm with three links will allow the openDog to interact with its environment.  This python script sets a path for the end-effector, calculates the four joint angles (controlled each by a motor) to achieve that path, and animates the result in 3D space as verification of the equations and requested path.  Shown below is a frame of the simulation window with the axes and angles defined. ![Arm Simulation](https://github.com/fainorr/opendog_IK/tree/master/images/arm_3d.png)

<image1 align="center">*Arm Simulation*: ![ ](https://github.com/fainorr/opendog_IK/tree/master/images/arm_3d.png "Arm Simulation")</image1>

2. IK_2D_v3: solves the inverse kinematics for a walking gait in 2-dimensions and animates the result.

3. IK_3D_plot3D: solves the inverse kinematics for a walking gait in 3-dimensions and animates the result on one 3-dimensional plot.  It also involves various walking gaits driven by an "action" and "direction".

4. lidar_test: plots sample LIDAR data and analyzes it for obstacle detection.
