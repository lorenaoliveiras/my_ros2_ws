#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file dict_utils.py
# @brief
#
# @author Júnio Eduardo de Morais Aquino

"""Module containing functions useful for dictionaries of substitutions."""

from typing import Dict, Text
from launch.utilities import normalize_to_list_of_substitutions
from launch import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.launch_context import LaunchContext

SomeSubstitutionTypeDict = Dict[SomeSubstitutionsType, SomeSubstitutionsType]
SubstitutionDict = Dict[Substitution, Substitution]


def normalize_substitution_dict(
        val: SomeSubstitutionTypeDict,
) -> SubstitutionDict:
    """
    Normalize a dictionary into a dictionary of substitutions.

    The resulting dictionary will contain Substitutions objects as both its
    keys and values.

    :param val: Dictionary to normalize.
    :return: A dictionary that contains Substitutions in its keys and values.
    """
    result = {}
    keys = normalize_to_list_of_substitutions(val.keys())
    vals = normalize_to_list_of_substitutions(val.values())

    for key, val in zip(keys, vals):
        result[key] = val
    return result

def describe_dict_substitutions(params: SubstitutionDict) -> Text:
    """
    Return a string containing the described keys and values.

    :param params: Dictionary of substitutions to describe.
    :return: String containing a description of the keys and values.
    """
    described_pairs = ["({}, {})".format(key.describe(), val.describe()) for
                       key, val in params.items()]
    return "dict_items([{}])".format(", ".join(described_pairs))


def perform_dict_substitutions(
        params: SubstitutionDict, context: LaunchContext
) -> Dict[Text, Text]:
    """
    Perform the substitutions in the keys and values of a dictionary.

    Receives a dictionary that contains substitutions in its keys and values,
    and a launch context, and returns a dictionary with the substitutions
    performed.

    :param params: Dictionary with substitutions in its keys and values.
    :param context: Launch context used to perform the substitutions.
    :return: A dictionary with the performed substitutions.
    """
    result = {}
    for key, val in params.items():
        result[key.perform(context)] = val.perform(context)
    return result
