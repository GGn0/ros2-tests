# ros2-tests

A workspace collecting some packages to learn ros2 functionalities

The file [NOTES.md](NOTES.md) contains a journal of the things I learned building this repo, together with links to the used resources.

The repo was build on Ubuntu 24.04

## Dependencies

Make sure to install the following packages before you go ahead:

- ROS2 - follow the [official guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- Gazebo - follow the [official guide](https://gazebosim.org/docs/harmonic/ros_installation/#summary-of-compatible-ros-and-gazebo-combinations)
- Rviz2 - `ros-${ROS_DISTRO}-rviz2`
- joint-state-publisher-gui - `ros-${ROS_DISTRO}-joint-state-publisher-gui`

## Examples list

The repo contains multiple example packages:

- [00_base_comm](#00-base-comm) - A launchfile example using demo publisher/subscriber nodes
- [01_simple_urdf](#01-simple-urdf) - A URDF robot description example.
- [02 URDF xacro](#02-urdf-xacro) - A URDF robot description example using xml macros.
- [03 Simple Gazebo](#03-simple-gazebo) - A robot in a Gazebo world.
- [04 ROS2 Control](#04-ros2-control) - Example package using ros2 control.
- [05 Gazebo ROS2 Control](#05-gazebo-ros2-control) - Example package using ros2 control in a Gazebo world.

For all the examples, it is assumed you have cloned the repository and you are in the workspace folder!

```sh
cd ~
git clone https://github.com/GGn0/ros2-tests/tree/main
cd ros2-tests
source /opt/ros/jazzy/setup.bash
colcon build --merge-install
```

> Note: replace jazzy with your ROS version

### 00 Base comm

Showcase a basic example of the usage of launch files to launch nodes.

It will launch nodes from `demo_nodes_cpp` and `demo_nodes_py` packages.

Open two terminals (on the same machine or on different machine on the same network).

(Terminal 1)

```sh
source install/setub.bash
ros2 launch ex00_base_comm listener.launch.py
```

(Terminal 2)

```sh
source install/setub.bash
ros2 launch ex00_base_comm talker.launch.py
```

### 01 Simple URDF

Showcase a basic example URDF robot description.

Run the example with:

```sh
ros2 launch ex01_simple_urdf simple_urdf.launch.py
```

### 02 URDF xacro

Showcase a parametric example of URDF robot description using xml macros.

Run the example with:

```sh
ros2 launch ex02_urdf_xacro urdf_xacro.launch.py
```

### 03 Simple Gazebo

Showcase a parametric example of URDF robot description using xml macros inserted in a Gazebo world.

Run the example with:

```sh
ros2 launch ex03_simple_gazebo simple_gazebo.launch.py
```

### 04 ROS2 control

Example configuration using ROS2 control.

Run the example with:

```sh
ros2 launch ex04_ros2_control ros2_control.launch.py
```

Test the movements with:

```sh
ros2 topic pub /diffbot_base_controller/cmd_vel geometry_msgs/msg/TwistStamped "{header: {frame_id: 'base_link'}, twist: {linear: {x: 1.6}, angular: {z: 2.4}}}" --rate 10
```

### 05 Gazebo ROS2 control

Example configuration using ROS2 control.

Run the example with:

```sh
ros2 launch ex05_gz_control gazebo.launch.py
```

Test the movements with:

```sh
ros2 topic pub /diffbot_base_controller/cmd_vel geometry_msgs/msg/TwistStamped "{header: auto, twist: {linear: {x: 0.70}, angular: {z: 1.4}}}" -1
```
