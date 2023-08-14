import os
import psutil
from typing import Optional
from warnings import warn

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def get_gzserver_pid() -> Optional[int]:
    """
    Check if the Gazebo server (gzserver) is running and return its PID.

    Returns
    -------
        Optional[int]: PID of the running gzserver process or None if gzserver
        is not running.

    """
    for proc in psutil.process_iter():
        if proc.name().strip().lower() == "gzserver":
            return proc.pid
    else:
        return None
    
def kill_gzserver():
    """If the Gazebo server is still running. Kill it."""
    gzserver_pid = get_gzserver_pid()
    if gzserver_pid is not None:
        proc = psutil.Process(gzserver_pid)
        proc.kill()

def generate_launch_description() -> LaunchDescription:

    return LaunchDescription([
        DeclareLaunchArgument(
                "MYROBOT.world",
                default_value="default.world",
                description="Name of the simulation world file. Must be a "
                "world of the provant_simulator_worlds package. "
                "If "
                "launching with a world from other package is "
                "desired, use "
                "the world argument instead.",
            ),
        DeclareLaunchArgument(
                "world",
                default_value=PathJoinSubstitution(
                    [
                        FindPackageShare("MYROBOT_gazebo"),
                        "worlds",
                        LaunchConfiguration("MYROBOT.world"),
                    ]
                ),
                description="Full path to the simulation world.",
            ),
        DeclareLaunchArgument(
                "verbose",
                default_value="true",
                description="Run Gazebo in verbose mode. If verbose mode "
                "is off, Gazebo will not output any messages, "
                "including "
                "errors.",
            ),
            DeclareLaunchArgument(
                "start_paused",
                default_value="true",
                description="Indicates if the simulation will start paused "
                "or not.",
            ),
            DeclareLaunchArgument(
                "respect_update_rates",
                default_value="true",
                description="If enabled, forces gazebo to respect the sensor"
                " update rates, slowing down the simulation real "
                "time rate if necessary.",
            ),
            DeclareLaunchArgument(
                "server_required",
                default_value="true",
                description="Makes the Gazebo server a required node. In "
                "this case if the Gazebo server dies during, "
                "the launch file will fail with an error.",
            ),
            DeclareLaunchArgument(
                "emulate_tty",
                default_value="true",
                description="Emulate a tty to ensure the output from Gazebo "
                "server is not buffered and printed directly to "
                "screen.",
            ),
            DeclareLaunchArgument(
                "gazebo_output",
                default_value="both",
                description="Indicates where the stdout and stderr outputs "
                "from Gazebo GUI and server are saved. By default the "
                "outputs are saved to the general launch file and to the "
                "screen.",
            ),
            SetEnvironmentVariable(
                name="OVERRIDE_LAUNCH_PROCESS_OUTPUT",
                value=LaunchConfiguration("gazebo_output"),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("gazebo_ros"),
                            "launch",
                            "gazebo.launch.py",
                        ]
                    )
                ),
                launch_arguments={
                    "pause": LaunchConfiguration("start_paused"),
                    "lockstep": LaunchConfiguration("respect_update_rates"),
                }.items(),
            ),
    ])