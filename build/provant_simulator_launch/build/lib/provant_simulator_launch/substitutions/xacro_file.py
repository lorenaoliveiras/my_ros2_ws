#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file xacro_str.py
# @brief This file contains the XACROSubstitution class.
#
# @author Júnio Eduardo de Morais Aquino
# TODO(jeduardo): Test this.

"""Module for the XACROSubstitution class."""

from typing import Text, Union, Dict, Optional
from launch import Substitution
from launch.launch_context import LaunchContext
import xacro
from xml.dom.minidom import Document
from provant_simulator_launch.utils.dict_utils import (
    SubstitutionDict,
    normalize_substitution_dict,
    perform_dict_substitutions,
    describe_dict_substitutions,
)


class XACROSubstitution(Substitution):
    """
    Process a file with XACRO and returned the process content as a string.

    This substitution receives a path to a file and an optional dictionary
    of arguments that will be passed to XACRO for usage with the processed
    file. The file will be processed using XACRO and a string with the
    resulting content returned.

    """

    def __init__(
        self,
        path: Union[Substitution, Text] = None,
        mappings: SubstitutionDict = None,
    ) -> None:
        """
        Construct a new XACRO Substitution.

        :param path: Path of the file to process.
        :param mappings: Optional list of arguments for usage with the file.

        """
        super().__init__()

        from launch.utilities import normalize_to_list_of_substitutions

        self.__mappings = {}
        if mappings is not None:
            self.__mappings = normalize_substitution_dict(mappings)

        self.__path = normalize_to_list_of_substitutions(path)[0]

    @property
    def path(self) -> Optional[Substitution]:
        """Return the path of the file to process."""
        return self.__path

    @property
    def mappings(self) -> Dict[Substitution, Substitution]:
        """Return a dictionary with parameters for the xacro processing."""
        return self.__mappings

    def describe(self) -> Text:
        """Return a string describing this substitution."""
        return "xacro.process_file({}, mappings={})".format(
            self.path.describe(), describe_dict_substitutions(self.mappings)
        )

    def perform(self, context: LaunchContext) -> Text:
        """
        Perform the substitution.

        Resolves the file path, and the mapping values, and call xacro to
        obtain the processed xml string.

        :param context: LaunchContext used to perform the substitution.
        :return: Resulting xml string from the xacro processing.

        """
        # Resolve the dict
        resolved_mappings = perform_dict_substitutions(self.mappings, context)

        # Resolve the file path and read it to an XML DOM Document
        resolved_path = self.path.perform(context)
        processed_doc: Document = xacro.process_file(
            resolved_path, mappings=resolved_mappings
        )
        return processed_doc.toxml()
