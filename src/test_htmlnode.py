import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_raise_tag_value_error(self) -> None:
        parent_node: ParentNode = ParentNode(None,
                                             [LeafNode("p", "no parent")])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_raise_children_value_error(self) -> None:
        parent_node: ParentNode = ParentNode("article", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_eq(self) -> None:
        parent_node: ParentNode = ParentNode(
                "section",
                [LeafNode("h1", "Heading"), LeafNode("p", "The paragraph.")],
                {"id": "testSection"})
        self.assertEqual(
                parent_node.to_html(),
                "<section id=\"testSection\">"
                + "<h1>Heading</h1>"
                + "<p>The paragraph.</p>"
                + "</section>")

    def test_nested_eq(self) -> None:
        section_node: ParentNode = ParentNode(
                "section",
                [
                    LeafNode("h1", "Heading"),
                    LeafNode("p", "First paragraph."),
                    LeafNode("p", "Second paragraph."),
                ])
        article_node: ParentNode = ParentNode(
                "article", [section_node, section_node, section_node])
        parent_node: ParentNode = ParentNode(
                "main", [article_node, article_node], {"id": "mainContent"})
        self.assertEqual(
                parent_node.to_html(),
                "<main id=\"mainContent\">"
                + "<article>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "</article>"
                + "<article>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "<section>"
                + "<h1>Heading</h1>"
                + "<p>First paragraph.</p>"
                + "<p>Second paragraph.</p>"
                + "</section>"
                + "</article>"
                + "</main>")
