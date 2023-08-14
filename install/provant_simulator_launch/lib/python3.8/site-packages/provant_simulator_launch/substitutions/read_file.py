#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file read_file.py
# @brief
#
# @author Júnio Eduardo de Morais Aquino

"""Module for the ReadFileSubstitution."""

from launch.substitution import Substitution
from launch.launch_context import LaunchContext
from typing import Union, Text


class ReadFileSubstitution(Substitution):
    """
    Read the content of a file and return its content.

    This substitution receives the path of a file, that can be specified as
    a substitution and thus only available at runtime, and returns a string
    containing the contents of the file when it is performed.

    Optionally, the encoding used by the file can be specified. By default,
    the UTF-8 encoding is used.

    """

    def __init__(
        self,
        path=Union[Substitution, Text],
        encoding: Union[Substitution, Text] = "utf-8",
    ) -> None:
        """
        Create a ReadFileSubstitution.

        :param path: Path of the file to read.
        :param encoding: Encoding used to read the file.

        """
        super().__init__()

        from launch.utilities import normalize_to_list_of_substitutions

        self.__path = normalize_to_list_of_substitutions(path)[0]
        self.__encoding = normalize_to_list_of_substitutions(encoding)[0]

    @property
    def path(self) -> Substitution:
        """Path of the file that will be read."""
        return self.__path

    @property
    def encoding(self) -> Substitution:
        """Get the encoding used to read the file."""
        return self.__encoding

    def describe(self) -> Text:
        """Return a description of this substitution."""
        return "open({}, 'r', encoding='{}').read()".format(
            self.path.describe(), self.encoding.describe()
        )

    def perform(self, context: LaunchContext) -> Text:
        """Resolve the path of the file, read it and return its content."""
        resolved_path = self.path.perform(context)
        resolved_encoding = self.encoding.perform(context)
        with open(resolved_path, "r", encoding=resolved_encoding) as file:
            return file.read()
