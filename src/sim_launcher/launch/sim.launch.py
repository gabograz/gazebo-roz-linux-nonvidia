import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    robot    = LaunchConfiguration("robot")
    world    = LaunchConfiguration("world")
    use_rviz = LaunchConfiguration("use_rviz")
#    spawn_x  = LaunchConfiguration("x")
#    spawn_y  = LaunchConfiguration("y")

    src_dir = "/home/ros2_ws/src"

    bridge_yaml = PathJoinSubstitution([src_dir, "robots", robot, "config", "bridge.yaml"])
    world_path  = PathJoinSubstitution([src_dir, "worlds", world])
    model_path  = PathJoinSubstitution([src_dir, "robots", robot, "model.sdf"])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_args": [world_path, " -r"]}.items(),
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        parameters=[{"config_file": bridge_yaml}],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-file", model_path,
#            "-name", robot,
#            "-x", spawn_x,
#            "-y", spawn_y,
            "-z", "0.2",
        ],
    )
    spawn_robot_delayed = TimerAction(period=3.0, actions=[spawn_robot])

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument("robot",
            default_value="tugbot",
            description="Nombre del robot en src/robots/"),
        DeclareLaunchArgument("world",
            default_value="empty.sdf",
            description="Nombre del archivo .sdf en src/worlds/"),
        DeclareLaunchArgument("use_rviz",
            default_value="true",
            description="Lanzar RViz2"),
#        DeclareLaunchArgument("x",
#            default_value="0.0",
#            description="Posición X del robot"),
#        DeclareLaunchArgument("y",
#            default_value="0.0",
#            description="Posición Y del robot"),
        gazebo,
        bridge,
        spawn_robot_delayed,
        rviz,
    ])