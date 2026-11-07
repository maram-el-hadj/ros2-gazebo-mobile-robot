import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    world = os.path.expanduser(
        '~/maram_ws/src/robot_basics/worlds/mon_monde.sdf')

    # 1. Gazebo
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world],
        output='screen')

    # 2. Bridge ROS 2 <-> Gazebo
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
        ],
        output='screen')

    return LaunchDescription([gazebo, bridge])
