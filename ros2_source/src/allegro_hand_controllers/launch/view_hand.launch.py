from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.parameter_descriptions import ParameterValue
import os

SOURCE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), *['..'] * 5)
)

print(f"Source directory: {SOURCE_DIR}")

def generate_launch_description():

    right_urdf_path = os.path.join(
        SOURCE_DIR,
        'install',
        'allegro_hand_description',
        'share',
        'allegro_hand_description',
        'urdf',
        'allegro_hand_description_right.urdf'
    )
    left_urdf_path = os.path.join(
        SOURCE_DIR,
        'install',
        'allegro_hand_description',
        'share',
        'allegro_hand_description',
        'urdf',
        'allegro_hand_description_left.urdf'
    )

    rviz_config_path = os.path.join(
        SOURCE_DIR,
        'src',
        'allegro_hand_controllers',
        'rviz',
        'hand.rviz'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            name='hand_side',
            default_value='left',
            description="Which hand to visualize: 'right' or 'left'"
        ),


        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': False}]
        ),


        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher_right',
            output='screen',
            parameters=[{

                'robot_description': ParameterValue(
                    Command(['cat ', right_urdf_path]),
                    value_type=str
                )
            }],
            condition=IfCondition(
                PythonExpression(["'", LaunchConfiguration('hand_side'), "' == 'right'"])
            )
        ),


        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher_left',
            output='screen',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['cat ', left_urdf_path]),
                    value_type=str
                )
            }],
            condition=IfCondition(
                PythonExpression(["'", LaunchConfiguration('hand_side'), "' == 'left'"])
            )
        ),


        ExecuteProcess(
            cmd=[
                'rviz2',
                '-d', rviz_config_path
            ],
            output='screen'
        )
    ])
