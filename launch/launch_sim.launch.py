#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python import get_package_prefix
from launch.substitutions import LaunchConfiguration
import xacro


def generate_launch_description():
    # Launch configurations

    # Add the path to the model to the Gazebo model path
    pkg_share_path = os.pathsep + \
        os.path.join(get_package_prefix('vacumoon_simulation'), 'share')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] = pkg_share_path
    print(os.getenv('GAZEBO_MODEL_PATH'))


    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Package and file paths
    pkg_example_simulation = get_package_share_directory('vacumoon_simulation')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Path to the empty.world file
    world_file_path = os.path.join(pkg_example_simulation, 'worlds', 'obstacles1.world')
    if not os.path.exists(world_file_path):
        raise FileNotFoundError(f"World file not found: {world_file_path}")


    # Xacro processing
    xacro_file = os.path.join(pkg_example_simulation, 'description', 'robot.urdf') # TODO integrate example for xacro
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Nodes
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, **robot_description}],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file_path}.items(),
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_bot'],
        output='screen',
    )


    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller'],
        output='screen',
    )

    position_forward_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_forward_controller'],
        output='screen',
    )

    joint_broad_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    # Launch description
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true',
        ),
        rsp_node,
        gazebo,
        spawn_entity,
        arm_controller_spawner,
        position_forward_spawner,
        joint_broad_spawner,
    ])
