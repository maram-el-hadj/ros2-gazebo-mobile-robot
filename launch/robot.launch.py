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
    #    /tf : transformation odom -> base_link publiee par DiffDrive
    #          (topic Gazebo /model/mon_robot/tf, renomme en /tf cote ROS 2)
    #    /clock : horloge de simulation
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/model/mon_robot/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
        ],
        remappings=[('/model/mon_robot/tf', '/tf')],
        output='screen')

    # 3. Transformation statique base_link -> lidar
    #    (le lidar est fixe sur le robot : x=0.1 m, z=0.23 m)
    #    Le nom du frame du lidar est celui lu dans le header de /scan.
    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0.1', '--y', '0', '--z', '0.23',
            '--roll', '0', '--pitch', '0', '--yaw', '0',
            '--frame-id', 'base_link',
            '--child-frame-id', 'mon_robot/lidar_link/lidar',
        ],
        output='screen')

    return LaunchDescription([gazebo, bridge, lidar_tf])
