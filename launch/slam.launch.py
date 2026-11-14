import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('robot_basics'),
        'config', 'slam_params.yaml')

    slam = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[config, {'use_sim_time': True}],
        output='screen')

    return LaunchDescription([slam])
