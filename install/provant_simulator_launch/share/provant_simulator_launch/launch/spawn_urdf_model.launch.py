#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# # This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
# Copyright 2022 Guilherme V. Raffo
##
# @file get_gazebo_models.py
# @brief Spawn a robot in gazebo.
#
# Used during testing of the step plugin.
#
# @author Júnio Eduardo de Morais Aquino

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import (
    AnonName,
    LaunchConfiguration,
)
from provant_simulator_launch.substitutions import JoinSubstitution


def generate_launch_description() -> LaunchDescription:
    """
    Spawn a robot in Gazebo.

    This launch description receives a required parameter that contains a
    path to a robot description file, either in URDF or SDF formats,
    a parameter that contains a name for the robot in Gazebo
    and optionally six parameters that specify the initial pose of the robot
    (x, y, z, roll, pitch, yaw).

    If the gazebo server node is running in a ROS namespace that is not the
    default one (the empty namespace), please specify the namespace of the
    gazebo node using the gazebo_namespace argument.

    Finally, it is also possible to specify a namespace for the ROS nodes
    created by the model plugins. By default, this namespace is
    /provant_simulator/<robot_name> where <robot_name> is the value
    specified in the parameter of the same name.

    :return:
    LaunchDescription
        A Launch description containing the necessary parameters, and a node
        that will wait for the Gazebo /spawn_entity service to become available
        and them call the service to launch a robot with the specified
        configuration.

    """
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_name",
                default_value="",
                description="The name of the robot in Gazebo.",
            ),
            DeclareLaunchArgument(
                "robot_namespace",
                default_value=JoinSubstitution(
                    [
                        "/provant_simulator/",
                        LaunchConfiguration("robot_name"),
                    ]
                ),
                description="The default namespace of the ROS node used by "
                            "the robot",
            ),
            DeclareLaunchArgument(
                "gazebo_namespace",
                default_value="",
                description="ROS namespace of the Gazebo server.",
            ),
            DeclareLaunchArgument(
                "robot_description_path", default_value="", description=""
            ),
            DeclareLaunchArgument(
                "x",
                default_value="0",
                description="Position of the robot along the x axis, "
                            "specified "
                            "in meters.",
            ),
            DeclareLaunchArgument(
                "y",
                default_value="0",
                description="Position of the robot along the y axis, "
                            "specified "
                            "in meters.",
            ),
            DeclareLaunchArgument(
                "z",
                default_value="0",
                description="Position of the robot along the z axis, "
                            "specified "
                            "in meters.",
            ),
            DeclareLaunchArgument(
                "roll",
                default_value="0",
                description="Rotation of the robot around the x axis. "
                            "Specified "
                            "in radians.",
            ),
            DeclareLaunchArgument(
                "pitch",
                default_value="0",
                description="Rotation of the robot around the y axis. "
                            "Specified "
                            "in radians.",
            ),
            DeclareLaunchArgument(
                "yaw",
                default_value="0",
                description="Rotation of the robot around the z axis. "
                            "Specified "
                            "in radians.",
            ),
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                name=AnonName(
                    name=(
                        "spawn_",
                        LaunchConfiguration("robot_name"),
                    ),
                ),
                arguments=[
                    "-entity",
                    LaunchConfiguration("robot_name"),
                    "-file",
                    LaunchConfiguration("robot_description_path"),
                    # "-package_to_model"  # Must be enabled to convert
                    # package:// URIS to model:// ones.
                    "-robot_namespace",
                    LaunchConfiguration("robot_namespace"),
                    # TODO(jeduardo): Conditionally add this argument
                    # " -gazebo_namespace",
                    # LaunchConfiguration("gazebo_namespace"),
                    "-x",
                    LaunchConfiguration("x"),
                    "-y",
                    LaunchConfiguration("y"),
                    "-z",
                    LaunchConfiguration("z"),
                    "-R",
                    LaunchConfiguration("roll"),
                    "-P",
                    LaunchConfiguration("pitch"),
                    "-Y",
                    LaunchConfiguration("yaw"),
                ],
            ),
        ]
    )
