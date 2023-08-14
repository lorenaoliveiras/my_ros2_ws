#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file join_substitution.py
# @brief This file contains the JoinSubstitution class.
#
# @author Júnio Eduardo de Morais Aquino
"""Module for the JoinSubstitution class"""

from typing import Iterable, Text, Union

from launch.substitution import Substitution
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.launch_context import LaunchContext
from launch.substitutions import SubstitutionFailure


class JoinSubstitution(Substitution):
    """
    Join strings and substitutions separated by a given character.

    This launch substitution accepts a sequence of texts or other
    substitutions and when executed will return a string containing formed
    by the join (concatenation) of the provided sequence separated by a
    specified string.

    By default, the separator is an empty string, meaning that the resulting
    join won't have any spaces
    """

    def __init__(self, substitutions: SomeSubstitutionsType,
                 sep: Union[Text, Substitution] = ""):
        """
        Create a Join Substitution.

        :param substitutions: A sequence of text or substitutions that will
        be joined (concatenated) into a single string. Must contain at least
        one element.
        :param sep: The separator character inserted between each element in
        the substitutions.
        :raises SubstitutionFailure: If an empty sequence of substitutions is
         provided.

        """
        super().__init__()
        if len(substitutions) == 0:
            raise SubstitutionFailure("An empty list of substitutions was "
                                      "received. At least one element is "
                                      "required.")
        from launch.utilities import normalize_to_list_of_substitutions
        self.__substitutions = normalize_to_list_of_substitutions(
            substitutions
            )
        self.__sep = normalize_to_list_of_substitutions(sep)[0]

    @property
    def substitutions(self) -> Iterable[Substitution]:
        """Getter for the substitutions to join."""
        return self.__substitutions

    @property
    def sep(self) -> Substitution:
        """Getter for the separating character."""
        return self.__sep

    def describe(self) -> Text:
        """Return a string that describes this substitution."""
        return "'{}'.join([{}])".format(
            self.sep, ', '.join(
                [s.describe() for s in
                 self.substitutions]
            )
        )

    def perform(self, context: LaunchContext) -> Text:
        """Perform this substitution."""
        performed_substitutions = [s.perform(context) for s in
                                   self.substitutions]
        resolved_sep = self.sep.perform(context)
        return resolved_sep.join(performed_substitutions)
