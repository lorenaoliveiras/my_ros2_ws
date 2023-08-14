#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file xacro_str.py
# @brief This file contains the XACROStrSubstitution class.
#
# @author Júnio Eduardo de Morais Aquino
# TODO(jeduardo): Test this.

"""Module for the XACROStrSubstitution class."""

from typing import Text, Union
from defusedxml.minidom import parseString
from launch import Substitution
from launch.launch_context import LaunchContext
import xacro
from xml.dom.minidom import Document
from provant_simulator_launch.utils.dict_utils import (
    describe_dict_substitutions,
    perform_dict_substitutions,
    SubstitutionDict,
    normalize_substitution_dict,
    SomeSubstitutionTypeDict,
)


class XACROStrSubstitution(Substitution):
    """
    Process a string with XACRO and return the resulting string.

    his substitution receives a string with the contents of a XACRO XML file
    and an optional dictionary of arguments that will be passed to XACRO for
    usage with the processed content. The input will be processed using XACRO
    and a string with the resulting content returned.

    """

    def __init__(
        self,
        content: Union[Substitution, Text] = None,
        mappings: SomeSubstitutionTypeDict = None,
    ) -> None:
        """
        Construct a XACROStrSubstitution object.

        :param content: A string with the contents of a valid XACRO file.
        :param mappings: Arguments passed to XACRO for processing of the
        content.

        """
        super().__init__()

        from launch.utilities import normalize_to_list_of_substitutions

        self.__content = normalize_to_list_of_substitutions(content)[0]

        self.__mappings = {}
        if mappings is not None:
            self.__mappings = normalize_substitution_dict(mappings)

    @property
    def content(self) -> Substitution:
        """Return the content of the file to process."""
        return self.__content

    @property
    def mappings(self) -> SubstitutionDict:
        """Return the arguments that will be passed to XACRO."""
        return self.__mappings

    def describe(self) -> Text:
        """Return a string describing this substitution."""
        return "xacro.process_doc({}, mappings={})".format(
            self.content.describe(), describe_dict_substitutions(self.mappings)
        )

    def perform(self, context: LaunchContext) -> Text:
        """
        Perform the substitution.

        Resolves the file content, and the mapping values, and call xacro to
        obtain the processed xml string.

        :param context: Context to perform the substitutions.
        :return: Resulting xml string from the xacro processing.

        """
        resolved_mappings = perform_dict_substitutions(self.mappings, context)

        # Resolve the file contents and read it to an XML DOM Document
        file_content = self.content.perform(context)
        doc = parseString(file_content)
        processed_doc: Document = xacro.process_doc(
            doc, mappings=resolved_mappings
        )
        return processed_doc.toxml()
