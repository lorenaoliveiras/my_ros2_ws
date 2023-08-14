#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# # This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
# Copyright 2022 Guilherme V. Raffo
##
# @file get_gazebo_models.py
# @brief Launches gazebo with the ProVANT Simulator default world.
#
# Used during testing of the wait until ready plugin.
#
# @author Júnio Eduardo de Morais Aquino

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
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


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


def format_gz_args(args: str) -> str:
    """
    Format a list of parameters into a colon separated string of unique paths.

    Args
    ----
        args (str): Original content of the Gazebo parameter.

    Returns
    -------
        str: A string containing a colon separated list of unique paths.

    """
    vals = args.split(":")
    res = set()
    for val in vals:
        stripped = val.strip()
        if len(stripped) > 0:
            res.add(stripped)
    return ":".join(res)


def generate_launch_description() -> LaunchDescription:
    """
    Generate a launch description containing a Gazebo simulator node.

    Returns
    -------
        LaunchDescription: ROS Launch description with a Gazebo server, Gazebo
        client, and parameters to specify the launched simulation world.

    """
    # Configure the Gazebo environment variables to allow loading the simulator
    # custom assets

    # Warn the user if the GAZEBO_RESOURCE_PATH is not set
    if os.environ.get("GAZEBO_MODEL_PATH") is None:
        warn(
            "The GAZEBO_MODEL_PATH environment variable is not set. It is "
            "recommended to source the /usr/share/gazebo/setup.sh script "
            "before running Gazebo with ROS2 for better compatibility."
        )

    # Check if Gazebo is running
    gzserver_pid = get_gzserver_pid()
    if gzserver_pid is not None:
        warn(
            "An instance of the gzserver process is running with pid=%d."
            "It is recommended to kill that process before starting another "
            "instance of the Gazebo server (gzserver) process."
        )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world_name",
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
                        FindPackageShare("provant_simulator_worlds"),
                        "worlds",
                        LaunchConfiguration("world_name"),
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
        ]
    )
