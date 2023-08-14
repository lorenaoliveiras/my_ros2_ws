# TODO(jeduardo): Implement this.

# Replace the package://something by absolute paths.
from typing import List, Text, Union

from launch.substitution import Substitution
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.launch_context import LaunchContext
from defusedxml.minidom import parseString
from xml.dom.minidom import Node as XMLNode
from ament_index_python import get_package_share_directory
import re


def replace_package(value: str) -> str:
    """
    Replace package:// URIs for file:// URIs.

    This function will check if the provided value contains a path starting
    with a package:// URI, typically used in ROS URDF files. If the string
    contains such a URL it will be replaced by an equivalent file:// URI
    with the absolute path of the indicated resource.

    The substitution uses the ROS2 ament index to get the location of the
    package share directory, and them replacing the package://<package_name>
    URI by file://<package_path> where <package_path> is the value returned
    by the ament index for a given <package_name>.

    :param value: String to replace the package:// URIs.
    :return: A string with any package://URIs replace by an equivalent
    file:// URI.

    """
    expr = re.compile(r"package://[^/]+")
    match = expr.search(value)
    if match is not None:
        package_str = value[match.start():match.end()]
        _, pkg_name = package_str.split("://")
        pkg_path = get_package_share_directory(pkg_name)
        if pkg_path.endswith('/'):
            pkg_path = pkg_path[:-1]
        file_uri = 'file://' + pkg_path
        value = value.replace(package_str, file_uri)
    return value


def replace_package_uris(dom: XMLNode) -> XMLNode:
    for node in dom.childNodes:
        if node.nodeType == XMLNode.TEXT_NODE:
            node.nodeValue = replace_package(node.nodeValue)
        elif node.nodeType == XMLNode.ELEMENT_NODE:
            for key, val in node.attributes.items():
                node.setAttribute(key, replace_package(val))
            replace_package_uris(node)
    return dom


class GazeboURDFSubstitution(Substitution):
    """

    """

    def __init__(self, xml: SomeSubstitutionsType) -> None:
        super().__init__()

        from launch.utilities import normalize_to_list_of_substitutions
        self.__xml = normalize_to_list_of_substitutions(xml)

    @property
    def xml(self) -> List[Substitution]:
        """Return the XML that will be processed."""
        return self.__xml

    def describe(self) -> Text:
        return super().describe()

    def perform(self, context: LaunchContext) -> Text:
        resolved_xml = ''.join([s.perform(context) for s in self.xml])

        xml_doc = parseString(resolved_xml)


        return resolved_xml
