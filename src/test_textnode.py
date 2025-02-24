import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        text_node1: TextNode = TextNode("This is a text node", TextType.TEXT)
        text_node2: TextNode = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(text_node1, text_node2)

    def test_repr_eq(self) -> None:
        text_node: TextNode = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(repr(text_node),
                         "TextNode(This is a text node, normal, None)")

    def test_link_eq(self) -> None:
        text_node: TextNode = TextNode("Boot dot dev", TextType.LINK,
                                       "https://www.boot.dev")
        self.assertEqual(repr(text_node),
                         "TextNode(Boot dot dev, link, https://www.boot.dev)")


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_eq(self) -> None:
        text_node: TextNode = TextNode("A normal text", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(text_node),
                         LeafNode(None, "A normal text"))

    def test_italic_eq(self) -> None:
        text_node: TextNode = TextNode("An italic text", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(text_node),
                         LeafNode("i", "An italic text"))

    def test_link_eq(self) -> None:
        text_node: TextNode = TextNode("Click me!", TextType.LINK,
                                       "https://www.boot.dev")
        self.assertEqual(
                text_node_to_html_node(text_node),
                LeafNode("a", "Click me!", {"href": "https://www.boot.dev"}))

    def test_image_eq(self) -> None:
        text_node: TextNode = TextNode(
                "Beautiful daisy flowers",
                TextType.IMAGE,
                "https://unsplash.com/photos/a-bunch-of-white-and-yellow-flowers-in-a-field-y-HLtKtZLqg")
        self.assertEqual(
                text_node_to_html_node(text_node),
                LeafNode("img", "",
                         {"src": "https://unsplash.com/photos/a-bunch-of-white-and-yellow-flowers-in-a-field-y-HLtKtZLqg",
                          "alt": "Beautiful daisy flowers"}))
