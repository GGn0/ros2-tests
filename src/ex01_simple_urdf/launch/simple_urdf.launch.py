import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'ex01_simple_urdf'
    file_subpath = 'description/diffdrivebot.urdf.xacro'

    # Read the description file
    with open(
        os.path.join(
            get_package_share_directory(pkg_name),
            file_subpath), 'r') as f:
        robot_description_raw = f.read()

    rviz_file = os.path.join(get_package_share_directory(pkg_name),
                             'description/rviz/config.rviz')
    # Configure the nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    node_joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_file]
    )

    # Run the nodes
    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher,
        node_rviz
    ])
