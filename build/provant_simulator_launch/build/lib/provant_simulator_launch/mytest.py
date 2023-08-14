from defusedxml.minidom import parseString
from defusedxml.ElementTree import fromstring
from xml.dom.minidom import Node as XMLNode
import re
from ament_index_python import get_package_share_directory
import os

# Read and parse the URDF document

xml_str = open(
    "/home/eduardo/dev_ws/src/provant_simulator_ros2"
    "/provant_simulator_models/provant_quadrotor/model.urdf"
).read()
xml_doc = parseString(xml_str)


matches = 0


def replace_package(value: str) -> str:
    expr = re.compile(r"package://[^/]+")
    match = expr.search(value)
    if match is not None:
        global matches
        matches += 1
        package_str = value[match.start():match.end()]
        _, pkg_name = package_str.split("://")
        pkg_path = get_package_share_directory(pkg_name)
        file_uri = 'file://' + pkg_path
        value = value.replace(package_str, file_uri)
    return value


def visit_all_nodes(dom: XMLNode, tabs: int = 0) -> XMLNode:
    for node in dom.childNodes:
        if node.nodeType == XMLNode.TEXT_NODE:
            node_val: str = node.nodeValue
            print('\t' * tabs, type(node), ": ", node_val.encode(), sep="")
            node.nodeValue = replace_package(node_val)
        elif node.nodeType == XMLNode.ELEMENT_NODE:
            print('\t' * tabs, type(node), " ", node.nodeName, sep="")
            for key, val in node.attributes.items():
                at = tabs + 1
                print(
                    '\t' * at, '<XML Attribute> ', key.encode(), ": ",
                    val.encode(),
                    sep=""
                    )
                node.setAttribute(key, replace_package(val))
            visit_all_nodes(node, tabs + 1)
        else:
            print('\t' * tabs, type(node), sep="")
    return dom


with open("test.urdf", "w") as file:
    file.write(visit_all_nodes(xml_doc).toxml())

print("Matches:", matches)
