# opendog_IK
During the 2019-2020 school year, the inverse kinematics and navigation sub-team of Lafayette's openDog senior design project worked on developing the **IK motion equations** and **LIDAR analysis techniques** in this repository.

## IK:

1. **ARM_IK_3D.py**: an arm with three links will allow the openDog to interact with its environment.  This python script sets a path for the end-effector, calculates the four joint angles (controlled each by a motor) to achieve that path, and animates the result in 3D space as verification of the equations and requested path.  A visual of the [**arm animation window**](https://github.com/fainorr/opendog_IK/tree/master/images/arm_3d.pdf) defines the links, axes, and angles.

2. **LEG_IK_3D.py**: for openDog locomotion, this script helps develop and visualize various walking gaits in a 3-dimensional animation.  Based on a chosen "action" from the options, it defines the gait parameters and leg phase shifts that accomplish the desired walking pattern, and then employs the three-dimensional inverse kinematic function to solve for the shoulder, femur, and tibia joint angles.  The [**3D walking gait**](https://github.com/fainorr/opendog_IK/tree/master/images/walk_3d.pdf) shows the limb mechanics and prints annotations for the leg in blue.  The angles and geometry are defined in a [**leg diagram**](https://github.com/fainorr/opendog_IK/tree/master/images/leg_model.pdf), where the x-axis points in the forward direction, the y-axis toward the body center, and the z-axis up.

3. **LEG_IK_2D.py**: this python script is a [**2D simplification**](https://github.com/fainorr/opendog_IK/tree/master/images/walk_2d.pdf) of the walking gait, which was used in the first attempts of making openDog walk.

4. **static_gait.py**: the walking tests on the real openDog were unsuccessful at first because the walking gait could not achieve stability; so, a static gait where the legs are moved individually was developed.  This script has a different set of foot position equations, but the IK function and animation are reproduced from the LEG_IK_3D.py script.
