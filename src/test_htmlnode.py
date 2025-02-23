import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr_eq(self) -> None:
        html_node: HTMLNode = HTMLNode(
                "div", "A generic node without children",
                props={"id": "noChildren"})
        self.assertEqual(
                repr(html_node),
                "HTMLNode(div, A generic node without children, None, "
                          + "{'id': 'noChildren'})")

    def test_props_to_html_eq(self) -> None:
        html_node: HTMLNode = HTMLNode(
                "div", "A generic node without children",
                props={"id": "noChildren"})
        self.assertEqual(html_node.props_to_html(), " id=\"noChildren\"")

    def test_children_eq(self) -> None:
        chilren_node: HTMLNode = HTMLNode("div", "children node")
        html_node: HTMLNode = HTMLNode(
                children=[chilren_node, chilren_node, chilren_node])
        self.assertEqual(
                repr(html_node),
                "HTMLNode(None, None, "
                          + "[HTMLNode(div, children node, None, None), "
                              + "HTMLNode(div, children node, None, None), "
                              + "HTMLNode(div, children node, None, None)], "
                          + "None)")
