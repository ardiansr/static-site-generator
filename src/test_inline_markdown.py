import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_raise_value_error(self) -> None:
        old_nodes: list[TextNode] = [
                TextNode("Sorry **forgot the second one", TextType.TEXT)]
        with self.assertRaisesRegex(
                ValueError, "Missing second '\\*\\*' delimiter"):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_delimiter_first_eq(self) -> None:
        old_nodes: list[TextNode] = [
                TextNode("**First delimiter** text", TextType.TEXT)]
        new_nodes: list[TextNode] = split_nodes_delimiter(
                old_nodes, "**", TextType.BOLD)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("First delimiter", TextType.BOLD),
                    TextNode(" text", TextType.TEXT),
                ])

    def test_delimiter_middle_eq(self) -> None:
        old_nodes: list[TextNode] = [
                TextNode("First text and *middle* delimiter", TextType.TEXT)]
        new_nodes: list[TextNode] = split_nodes_delimiter(
                old_nodes, "*", TextType.ITALIC)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("First text and ", TextType.TEXT),
                    TextNode("middle", TextType.ITALIC),
                    TextNode(" delimiter", TextType.TEXT),
                ])

    def test_text_between_eq(self) -> None:
        old_nodes: list[TextNode] = [
                TextNode("`char *code;` and `size_t len;`", TextType.TEXT)]
        new_nodes: list[TextNode] = split_nodes_delimiter(
                old_nodes, "`", TextType.CODE)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("char *code;", TextType.CODE),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("size_t len;", TextType.CODE),
                ])
