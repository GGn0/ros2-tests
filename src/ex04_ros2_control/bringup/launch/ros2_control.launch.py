from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_name = 'ex04_ros2_control'
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

    robot_description_params = {"robot_description": robot_description}  # ,
    #                           "use_sim_time": True}

    # Controllers
    # Load the controller configurations
    # (Controller manager + motion controller + joint state broadcaster)
    robot_controllers = PathJoinSubstitution([
        FindPackageShare(pkg_name),
        "config",
        controllers_name
    ])

    # RVIZ config file
    rviz_config = PathJoinSubstitution([
        FindPackageShare(pkg_name),
        "rviz",
        "rviz_conf.rviz"
    ])

    #########
    # NODES #
    #########

    # Controller manager
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="both",
        parameters=[robot_description_params, robot_controllers]
    )

    # State publisher node
    robot_state_pub_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description_params]
    )

    # RviZ node
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config]
    )

    ############
    # SPAWNERS #
    ############

    # Spawners are one-shot nodes which putposes is to launch other nodes
    # We can use them to define a launch sequence using events
    # x_node is launched by x_node_spawner
    # on exit of x_node_spawner we launch y_node_spawner

    # The sequence we want to attain is:
    # joint_state_broadcaster -> robot_controller
    # joint_state_broadcaster -> RVIz

    # Joint state broadcast spawner
    joint_state_br_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ]
    )

    # Robot controller spawner
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diffbot_base_controller",
            "--controller-manager",
            "/controller_manager"
        ]
    )
    #         "--param-file",
    #         yaml_file,
    #         "--controller-ros-args",
    #         "-r /diffbot_base_controller/cmd_vel:=/cmd_vel",
    #     ],
    # )

    #############
    # SEQUENCES #
    #############

    # Rviz sequence
    seq_rviz_after_joint_st_br = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_br_spawner,
            on_exit=[rviz_node]
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
        control_node,
        robot_state_pub_node,
        joint_state_br_spawner,
        seq_robot_controller_after_joint_st_br,
        seq_rviz_after_joint_st_br
    ])
