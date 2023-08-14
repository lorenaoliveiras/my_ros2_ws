#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This file is part of the ProVANT simulator project.
# Licensed under the terms of the MIT open source license. More details at
# https: //github.com/Guiraffo/ProVANT-Simulator/blob/master/LICENSE.md
##
# @file callable.py
# @brief This file contains the CallableSubstitution and supporting functions.
#
# @author Júnio Eduardo de Morais Aquino

"""Module for the CallableSubstitution class and supporting functions."""

from typing import Callable, Text, Tuple, Dict, Any
from launch.substitution import Substitution
from launch.launch_context import LaunchContext


def perform_if_sub(arg, context: LaunchContext) -> Any:
    """
    Return the result of a substitution or a value.

    Check if the provided argument is a launch substitution, if it is
    perform the substitution and return its value. If it is not, return the
    argument itself, without modification.

    :param arg: Value to check and perform substitution.
    :param context: Context for the substitution.
    :return: Result of the substitution or the value itself.

    """
    if isinstance(arg, Substitution):
        return arg.perform(context)
    else:
        return arg


def perform_arg_substitution(args: Tuple, context: LaunchContext) -> Tuple:
    """
    Perform the substitutions in a tuple of arguments.

    This method will iterate over the tuple, check if its elements are
    launch substitutions, and if they are, perform it and return their value.
    The elements which are not launch substitutions are returned without
    modification.

    :param args: Tuple of arguments to perform the substitutions.
    :param context: Context for the substitutions.
    :return: Tuple in which the substitutions elements are replaced by the
    result of its evaluation.

    """
    return tuple([perform_if_sub(arg, context) for arg in args])


def perform_kwargs_substitution(kwargs: Dict, context: LaunchContext) -> Dict:
    """
    Perform the substitutions in a dictionary of arguments.

    Check if the key and or value of a dictionary element is a substitution,
    and if it is, perform it and return the resulting value. If it is not,
    return the value itself without modification.

    :param kwargs: Dictionary to perform the substitution.
    :param context: Context to perform the substitutions.
    :return: Dictionary in which every substitution was performed, and replaced
    by its resulting value.

    """
    result = {}
    for key, val in kwargs.items():
        result[perform_if_sub(key, context)] = perform_if_sub(val, context)
    return result


def describe_if_substitution(element) -> Text:
    """Return a string describing the provided element."""
    if isinstance(element, Substitution):
        return element.describe()
    else:
        return repr(element)


def describe_args(args: Tuple) -> Text:
    """Return a string describing the provided sequence of arguments."""
    return ", ".join([describe_if_substitution(arg) for arg in args])


def describe_kwargs(args: Dict) -> Text:
    """Return a string describing the provided dictionary of arguments."""
    elements = []
    for key, val in args.items():
        "{} = {}".format(
            describe_if_substitution(key), describe_if_substitution(val)
        )
    return ", ".join(elements)


class CallableSubstitution(Substitution):
    """
    A substitution that executes a provided python callable.

    The Callable Substitution accepts a python callable object, a sequence of
    arguments and a dictionary of named arguments that will be passed to the
    callable when the substitution is executed.

    The arguments and named arguments can contain substitutions, the latter
    accepting them in both its keys and values. These substitutions will be
    performed prior to the execution of the provided callable.

    """

    def __init__(
        self,
        call: Callable[..., Text],
        args: Tuple = None,
        kwargs: Dict = None,
    ) -> None:
        """
        Construct a Callable Substitution.

        :param call: A callable that will be executed when the substitution
        is performed.
        :param args: Arguments to pass to the callable. May contain
        substitutions.
        :param kwargs: Named arguments (kwargs) to pass to the callable. May
        contain substitutions in both the keys and values.

        """
        super().__init__()
        self.__callable = call
        self.__args = args
        if args is None:
            self.__args = tuple()
        self.__kwargs = kwargs
        if kwargs is None:
            self.__kwargs = {}

    @property
    def callable(self) -> Callable[..., Text]:
        """Return the method that will be called by the substitution."""
        return self.__callable

    @property
    def args(self) -> Tuple:
        """Return the arguments that will be passed to the callable."""
        return self.__args

    @property
    def kwargs(self) -> Dict:
        """Return the named arguments that will be passed to the callable."""
        return self.__kwargs

    def describe(self) -> Text:
        """Return a string describing the current action."""
        return "{}({}, {})".format(
            repr(self.callable),
            describe_args(self.args),
            describe_kwargs(self.kwargs),
        )

    def perform(self, context: LaunchContext) -> Text:
        """
        Call the provided callable with the specified args and kwargs.

        Perform any substitution present in the args and kwargs, and call
        the provided callable passing the resulting arguments.

        :param context: Context to perform the substitution
        :return: String returned by the execution of the provided method.

        """
        # Perform args substitution
        resolved_args = perform_arg_substitution(self.args, context)
        resolved_kwargs = perform_kwargs_substitution(self.kwargs, context)
        return self.callable(*resolved_args, **resolved_kwargs)
