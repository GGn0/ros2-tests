# LEARNING JOURNAL

This file will contain notes and resources used to build the example packages

## Sourcing

When working with ros2, you have to remember to source your ros version.

This means setting up the necessary environment variables (including PATH) with the following command:

> Replace jazzy with your ros2 version name!

```sh
source /opt/ros/jazzy/setup.bash
```

## Workspace

While developing with ROS2, it is common practice to create a workspace folder and a source folder `src` within it.

The code for the packages you develop, will be eack in a subfolder of src.

```none
myRosDev_ws
  │
  ├─ src
  │    │
  │    ├─ package1
  │    │
  │    ├─ package2
  │    ...
  ├─ other build artifacts
  .
  .
  .
  ```

Setup you starting folder structure:

```sh
mkdir -p ~/myRosDev_ws/src
```

> NOTE!
> This is not needed if you are cloning this repo. The cloned repo itself is the workspace.

## Packages

Packages are a collection of your nodes, launchfiles, etc...

### Initialize a package

To first create a package, `cd` into the `src` folder of you workspace and run the `pkg` command.

```sh
cd ~/myRosDev_ws/src
ros2 pkg create --build-type ament_python PACKAGE_NAME
```

Populate the automatically generated `package.xml` and `setup.py` files with your contact info and the package description.

A more complete command is the following:

```sh
ros2 pkg create --build-type ament_python PACKAGE_NAME --build-type ament_python --license LICENSE --maintainer-email YOUR_EMAIL --description 'PACKAGE_DESCRIPTION'
```

### Write your robot description

Robot descriptions are written in XML format using URDF files.

These include links and joints, specifying visual geometry, collision boxes and inertial information.

It is possible (and reccomended) to split your descriptions in multiple files and reuse common descriptions (e.g. colors definitions).

arrange your launch files in the `src/PACKAGE_NAME/description` folder

> Common practice is to name the launch files as: `NAME.urdf.xacro`

### Write your launch files

Launch files allow you to automate multiple tasks, for example running multiple nodes.

arrange your launch files in the `src/PACKAGE_NAME/launch` folder

> Common practice is to name the launch files as: `NAME.launch.py`

```sh
cd ~/myRosDev_ws/src/PACKAGE_NAME
cd mkdir launch
touch launch/NAME.launch.py
touch launch/NAME1.launch.py
...
```

To make the launch files available after building your package, you have to specify them in the `setup.py` script located under `src/PACKAGE_NAME`

```python
from glob import glob
...
    data_files=[
        ...,
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/description',
         glob('description/*.urdf.xacro')),
    ],
...
```

This instructs `colcon` at build time, to copy (or link) any file under `src/PACKAGE_NAME/launch/` matching the pattern `*.launch.py` to the folder `install/PACKAGE_NAME/share/PACKAGE_NAME/launch`

See the code or the resources for some examples on how to write the launch files.

### Build your package

To build our packages, we use `colcon`.

Make sure to add your package dependencies to `package.xml`

From the workspace directory, we can either build all the packages or just one.

All the packages:

```sh
cd ~/myRosDev_ws
colcon build --symlink-install
```

Just one package:

```sh
cd ~/myRosDev_ws
colcon build --packages-select PACKAGE_NAME
```

> Notes:
>
> - `--symlink-install` will create symbolic links to source files. If you are having issues running the package after the build, consider adding the `--cmake-clean-cache` flag to make a clean build.
> - When building for deployment, you want to copy the src files instead of linking them, so use `--merge-install` instead

### Run nodes of yor package

After building your package, you have to source it, then you can run the code it contains!

```sh
cd ~/myRosDev_ws
source install/setup.bash
ros2 launch PACKAGE_NAME LAUNCHFILE.py
```

## Notes on specific exercises

### 01 simple urdf

Look at the [launch file](src/ex01_simple_urdf/launch/simple_urdf.launch.py) first

In this exercise, we are using the `state_publisher` node of the `state_publisher` package in which we feed our description as a parameter.

It will look for the fixed joints and publish messages about their state.

Similarly, for dynamic joints, we are using `joint_state_publisher_gui` node from the `joint_state_publisher_gui` package, which is also creating topics to control the joints.

This launch file also contains an rviz configuration.

> Note: the parameter fed to the state_publisher node, is the xml content of the descriptor, not its path!

After that, take a look at the [description file](src/ex01_simple_urdf/description/diffdrivebot.urdf.xacro) to see how the links and hoints are configured

**Link geometry origin**
When moving your origin consider that:

- The origin is located at the center of gravity of the geometry
- When you specify `<origin xyz="...">` offset, these will be the new coordinates of the CoG

**Joints axis**
The joint axis tag defines the axis along which the joints moves. It refers to the axis of the child link.

### 02 URDF xacro

One of the issue with the previous example was the repeating pieces of code, for example the same sizes and origins for geometry and collision tags.

read the [description file](src/ex02_urdf_xacro/description/diffdrivebot.urdf.xacro)

- The file [diffdrivebot_params.xacro](src/ex02_urdf_xacro/description/diffdrivebot_params.xacro) contains a list of properties like mass and size of different links.
- The file [inertial_calculations.xacro](src/ex02_urdf_xacro/description/inertial_calculations.xacro) contains macros to calculate inertia tensors and fill the `<inertial>` tag.
- The file [material.xacro](src/ex02_urdf_xacro/description/materials.xacro) contains color definitions.

From there look at the other referenced description files.

Finally, take a look at the [launch file](src/ex02_urdf_xacro/launch/urdf_xacro.launch.py) in which the main xacro file had to be interpreted first and then passed to the `state_publisher`

This launch file also contains an rviz configuration.

### 03 Simple Gazebo

Differences to example 02:

**Descriptors**
These changes are reflected in the [gazebo_config.xacro](src/ex03_simple_gazebo/description/gazebo_config.xacro) file:

- Gazebo-specific color definition attached to the links
- Joint state published by Gazebo and not by the `joint_state_publisher_gui`

**Launchfiles**
The [launch file](src/ex03_simple_gazebo/launch/simple_gazebo.launch.py) includes a gazebo node (through its own [launch file](src/ex03_simple_gazebo/launch/gazebo_launch.launch.py)) and the spawn node.

The gazebo node will launch gazebo with the empty world.

The spawn node takes in the topic to which to subscribe to display the robot states.
In our case, it is `robot_description` generated by `robot_state_publisher`

### 04 Basic ROS Control

According to the [official documentation](https://control.ros.org/master/doc/getting_started/getting_started.html), we need to go through 3 steps:

>
>1. Create a YAML file with the configuration of the controller manager and two controllers.
>
>2. Extend the robot’s URDF description with needed `<ros2_control>` tags. It is recommended to use macro files (xacro) instead of pure URDF.
>
>3. Create a launch file to start the node with Controller Manager. You can use a default ros2_control node (recommended) or integrate the controller manager in your software stack.

The file structure is as follows:

```none
src/package_folder
 │ └─ bringup (folder containing configurations)
 │    │
 │    ├─ config
 │    │    └──robot-controllers.yaml (see [section 04.1](#041-yaml-file))
 │    │
 │    └── launch
 │         └── launchfile.launch.py (launchfile to start all the necessary nodes)
 │
 ├─ description
 │    │
 │    ├─ ros2_control
 │    │    ├─diffbot.ros2_control.xacro (define the hardware interfaces)
 │    │
 │    └── urdf
 │         ├─ robot.urdf.xacro
 │         └── ... (other xaxro utilities)
 .
 .
 .
```

#### 04.1 YAML file

The YAML file contains the configuration of the **controller manager** and other controllers (we are using a differential robot controller, other controllers are available in the [official controllers index](https://github.com/ros-controls/ros2_controllers/blob/master/doc/controllers_index.rst)).

Together with the controller manager, we also initialize the **joint state broadcaster** to make robot joint states available.

#### 04.2 URDF description

First we create the parameters xacro file.

We can take most from exercise 3.

One difference is that some parameters will be defined in the YAML config of step 1.

Therefore, these parameters will be read from the YAML itself.

Note:The base link will be at the center of the wheel axis.

In addition to that, we have to add the ros2_control tags, which are included with a xacro macro.
The tags define the interface between the controllers and the joints (a mock_component is used to simulate motors feedback)

#### 04.3 Launch file

The launch file will start the control manager, the differential robot controller node, the state publisher (to get joint states), the joint broadcaster (to get the joint frames), rviz to visualize everything.

A rviz has been built from the tool and saved to be then loaded by the launchfile.

The launchfile also uses event handlers to define a proper startup. (state publisher before rviz and the robot controller)

#### 04.4 Setup.py and package.xml

Finally we have to make all these files available after build by modifying the setup.py script

We also add all the used packages to the dependencies in package.xml

### 05 Gazebo ROS control

Differences with exercise 04:

- [05.1](#051-gazebo-launcher) Added a Gazebo specific launch file and removed the old one
- [05.2](#052-urdf-descriptor) Updated the urdf robot descriptor
- [05.3](#053-gazebo-world) Added a Gazebo world
- [05.4](#054-configs) Added/modified yaml configuration files

Updates to package.xml and setup.py

#### 05.1 Gazebo launcher

The main additions are:

- Removed Rviz config and node
- Load Gazebo world settings
- Load Gazebo bridge settings
- Setup Gazebo simulator node
- Setup Gazebo bridge node
- Setup robot (entity) spawner node
- Launch sequence change: Entity spawn -> joint state broadcaster -> controller

> NOTE: the parameter `--controller-manager /controller_manager` has been removed from the controller and joint state broadcaster nodes as it lead to errors.

#### 05.2 URDF descriptor

The main additions are:

- Gazebo materials (colors and friction coefficients) in [materials.xacro](src/ex05_gz_control/description/urdf/materials.xacro)
- Plugin (ROS2_control) to define the hardware interface using Gazebo engine [diffbot.ros2_control.xacro](src/ex05_gz_control/description/ros2_control/diffbot.ros2_control.xacro)
- Plugin (Gazebo) to use ros2_control controllers in Gazebo [diffbot.ros2_control.xacro](src/ex05_gz_control/description/ros2_control/diffbot.gazebo.xacro)

> Note: I had to rotate one of the wheels in the robot descriptor because it was wrongly configured

#### 05.3 Gazebo world

An empty world has been added to the new `world` folder. This contains a solid plane to allow the robot to stand on.

#### 05.4 Configs

Added the [gz_bridge.yaml](src/ex05_gz_control/bringup/config/gz_bridge.yaml) configuration file, determining which topics are mapped from ROS2 to Gazebo (and vice versa)

Modified the [robot_controllers.yaml](src/ex05_gz_control/bringup/config/robot_controllers.yaml) configuration file.

Set the joint state broadcaster to use simulation time and set the differential drive controller outside the controller manager.

## Resources

[@ArticulatedRobotics playlist](https://www.youtube.com/watch?v=2lIV3dRvHmQ&list=PLunhqkrRNRhYYCaSTVP-qJnyUPkTxJnBt&pp=0gcJCbAEOCosWNin) on Youtube.

@ArticulatedRobotics videos ([1](https://www.youtube.com/watch?v=BcjHyhV0kIs), [2](https://www.youtube.com/watch?v=IjFcr5r0nMs)) on differential drive robot modeling

[ROS2 Documentation - Packages](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

[ROS2 Documentation - Launch Files](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)

[ROS2 Documentation - URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html)
