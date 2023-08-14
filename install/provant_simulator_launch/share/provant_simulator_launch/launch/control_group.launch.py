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
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package="provant_simulator_simulation_manager",
            executable="provant_simulator_simulation_manager_node",
            name="simulation_manager",
            namespace="/provant_simulator"
        )
    ])
