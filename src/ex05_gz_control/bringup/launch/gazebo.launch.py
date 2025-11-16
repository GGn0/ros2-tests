from os import path
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import RegisterEventHandler, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_name = 'ex05_gz_control'
    urdf_name = 'diffdrivebot.urdf.xacro'
    controllers_name = 'robot_controllers.yaml'

    # URDF robot description
    # interpret the xacro file
    # It will run the 'xacro xacro_file' command
    # It will point to the xacro file in the install folder!
    # (be consistent to setup.py)
    robot_description = Command([
        PathJoinSubstitution([FindExecutable(name='xacro')]),
        " ",
        PathJoinSubstitution([
            FindPackageShare(pkg_name),
            "description",
            urdf_name
        ])
    ])

    robot_description_params = {"robot_description": robot_description}

    # Controllers
    # Load the controller configurations
    # (Controller manager + motion controller + joint state broadcaster)
    robot_controllers = PathJoinSubstitution([
        FindPackageShare(pkg_name),
        "config",
        controllers_name
    ])

    # Gazebo world config file
    world_file = PathJoinSubstitution([
        FindPackageShare(pkg_name),
        "worlds",
        "empty.sdf"
    ])

    # Gazebo bridge config
    gz_bridge_params = path.join(
        get_package_share_directory(pkg_name),
        'config/gz_bridge.yaml')

    #########
    # NODES #
    #########

    # Start Gazebo
    gz_sim_launchfile = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
                ])
        ]),
        launch_arguments={
            'gz_args': ['-r -v4 ', world_file],
            'on_exit_shutdown': 'true',
        }.items()
    )

    # Gazebo bridge
    ros_gz_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        # arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={gz_bridge_params}',
        ]
    )

    # State publisher node
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description_params]
    )

    ############
    # SPAWNERS #
    ############

    # Spawners are one-shot nodes which putposes is to launch other nodes
    # We can use them to define a launch sequence using events
    # x_node is launched by x_node_spawner
    # on exit of x_node_spawner we launch y_node_spawner

    # The sequence we want to attain is:
    # Gazebo sim -> joint state broadcaster
    # joint_state_broadcaster -> robot_controller

    # Joint state broadcast spawner
    joint_state_br_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster"
        ]
    )

    # Robot controller spawner
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diffbot_base_controller",
            "--param-file", robot_controllers
        ]
    )

    # Spawn robot in Gazebo Harmonic
    robot_spawner = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "/robot_description",
            "-name", "robot",
            "-z", "0.2"
        ],
    )

    #############
    # SEQUENCES #
    #############

    # Joint state broadcaster sequence
    seq_joint_st_br_after_gz = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=robot_spawner,
            on_exit=[joint_state_br_spawner]
        )
    )

    # controller sequence
    seq_robot_controller_after_joint_st_br = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_br_spawner,
            on_exit=[robot_controller_spawner]
        )
    )

    # Run the nodes
    return LaunchDescription([
        gz_sim_launchfile,
        ros_gz_bridge_node,
        robot_spawner,
        robot_state_pub_node,
        seq_joint_st_br_after_gz,
        seq_robot_controller_after_joint_st_br,
    ])
