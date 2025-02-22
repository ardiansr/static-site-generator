import unittest

from textnode import TextNode, TextType


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
