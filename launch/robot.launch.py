import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    world = os.path.expanduser(
        '~/maram_ws/src/robot_basics/worlds/mon_monde.sdf')

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world],
        output='screen')

    return LaunchDescription([gazebo])
