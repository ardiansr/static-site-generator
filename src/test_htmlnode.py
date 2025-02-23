import unittest

from htmlnode import HTMLNode, LeafNode


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


class TestLeafNode(unittest.TestCase):
    def test_raise_value_error(self) -> None:
        leaf_node: LeafNode = LeafNode("p", None)
        self.assertRaises(ValueError, leaf_node.to_html)

    def test_eq(self) -> None:
        leaf_node: LeafNode = LeafNode("a", "Click me!",
                                       {"href": "https://www.boot.dev"})
        self.assertEqual(
                leaf_node.to_html(),
                "<a href=\"https://www.boot.dev\">Click me!</a>")

    def test_no_attr_eq(self) -> None:
        leaf_node: LeafNode = LeafNode("p", "This is a paragraph text.")
        self.assertEqual(leaf_node.to_html(),
                         "<p>This is a paragraph text.</p>")
