import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # Command-line arguments

    description_file = os.path.join(
        get_package_share_directory("allegro_hand_description"), "urdf", "allegro_hand_description_right.urdf"
    )

    rviz_file = os.path.join(
        get_package_share_directory("allegro_hand_controllers"), "rviz", "hand.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        parameters=[
            description_file,
        ],
        arguments=['-d'+str(rviz_file)]
    )
    return LaunchDescription(
        [

            rviz_node,

        ]
    )
