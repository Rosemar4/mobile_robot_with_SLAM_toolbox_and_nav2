import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('slam_robot')
    nav2_dir = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    params_file = LaunchConfiguration('params_file', default=os.path.join(pkg_share, 'config', 'nav2_params.yaml'))
    map_file = LaunchConfiguration('map', default=os.path.join(pkg_share, 'maps', 'my_map.yaml'))

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_dir, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'map': map_file
        }.items()
    )

    return LaunchDescription([
        nav2_launch
    ])
