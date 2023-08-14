from xml.dom.minidom import Node as XMLNode


def remove_comments(dom: XMLNode):
    for node in dom.childNodes:
        if len(node.childNodes) == 0:
            if node.nodeType == XMLNode.COMMENT_NODE:
                node.parentNode.removeChild(node)
        else:
            for child in node.ChildNodes:
                remove_comments(child)


def remove_whitespace(dom: XMLNode):
    for node in dom.childNodes:
        if node.nodeType == XMLNode.TEXT_NODE:
            if node.nodeValue:
                node.nodeValue = node.nodeValue.strip()
        elif node.nodeType == XMLNode.ELEMENT_NODE:
            remove_whitespace(node)