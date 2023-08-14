#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file simulation_manager.launch.py
# @brief A launch script to spawn the simulation manager node
#
# @author Júnio Eduardo de Morais Aquino

from launch.launch_description import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    robot_name = "quad"

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("provant_simulator_launch"),
                            "launch",
                            "gazebo.launch.py"
                        ]
                    ),
                )
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("provant_simulator_launch"),
                            "launch",
                            "spawn_urdf_model.launch.py"
                        ]
                    ),
                ),
                launch_arguments=[
                    ("robot_name", robot_name),
                    ("robot_description_path", PathJoinSubstitution(
                        [
                            FindPackageShare("provant_quadrotor"),
                            "gz_model",
                            "provant_quadrotor",
                            "model.urdf"
                        ]
                    )),
                    ("z", "0.032891"),
                ],
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("provant_simulator_launch"),
                            "launch",
                            "simulation_manager.launch.py"
                        ]
                    )
                )
            ),
            Node(
                package="provant_simulator_control_group_manager",
                executable="provant_simulator_control_group_manager",
                namespace="/provant_simulator/" + robot_name,
                name="control_group_manager",
                parameters=[
                    {"control_step": 0.012},
                ],
            ),
            Node(
                package="provant_simulator_reference_generator",
                executable="ref_gen_node",
                namespace="/provant_simulator/" + robot_name,
                name="reference_generator",
            ),
            Node(
                package="provant_simulator_lqr_quadcopter",
                executable="lqr_quadcopter_node",
                namespace="/provant_simulator/" + robot_name,
                name="controller"
            ),
            Node(
                package="provant_simulator_zoh",
                executable="control_zoh_node",
                namespace="/provant_simulator/" + robot_name,
                name="control_inputs_zoh",
                parameters=[
                    {"actuators": [
                        "propeller1",
                        "propeller2",
                        "propeller3",
                        "propeller4",
                    ]},
                    {"initial_value": [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                    ]},
                ],
            ),
        ]
    )
