import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_share = FindPackageShare(package='slam_robot').find('slam_robot')
    world_path = os.path.join(pkg_share, 'worlds', 'rectangular_world.sdf')
    urdf_path = os.path.join(pkg_share, 'urdf', 'slam_robot.xacro')

    # Start Gazebo Ignition
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world_path],
        output='screen'
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'slam_robot',
            '-file', urdf_path,
            '-x', '0', '-y', '0', '-z', '0.1'
        ],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(urdf_path).read()}],
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
        spawn_robot,
        robot_state_publisher,
        bridge
    ])
