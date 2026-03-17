# launch/gazebo.launch.py
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('slam_robot')
    world_path = os.path.join(pkg_share, 'worlds', 'rectangular_world.sdf')

    # Launch Gazebo Ignition with your world
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world_path],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(os.path.join(pkg_share, 'urdf', 'slam_robot.xacro')).read()}],
        output='screen'
    )

    # ROS-GZ Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
            '/tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock@ignition.msgs.Clock',
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        bridge
    ])
