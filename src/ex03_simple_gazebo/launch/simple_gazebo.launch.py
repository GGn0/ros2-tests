import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'ex03_simple_gazebo'
    file_subpath = 'description/diffdrivebot.urdf.xacro'

    # Process the file with xacro
    xacro_file = os.path.join(get_package_share_directory(pkg_name),
                              file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Configure the nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
                     'use_sim_time': True}]
    )

    # This will include the content of the launch file gazebo_launch.launch.py
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch',
                         'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # The spawn node will spawn an entity and show its links
    # according to the topic given as a parameter
    # robot is the name of the robot specified in the URDF file
    launch_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch',
                         'gz_spawn_model.launch.py')),
        launch_arguments={'topic': 'robot_description',
                          'entity_name': 'robot'}.items()
    )

    # Run the nodes
    return LaunchDescription([
        node_robot_state_publisher,
        launch_gazebo,
        launch_spawn
    ])
