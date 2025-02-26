import unittest

from inline_markdown import (extract_markdown_images, extract_markdown_links,
                             split_nodes_delimiter, split_nodes_image,
                             split_nodes_link, text_to_textnodes)
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_eq(self) -> None:
        text: str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
                text_to_textnodes(text),
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE,
                             "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ])

    def test_second_eq(self) -> None:
        text: str = "This is _text_ with an **bold** word and a `code block` and a [link](https://boot.dev) and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
                text_to_textnodes(text),
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.ITALIC),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE,
                             "https://i.imgur.com/fJRm4Vk.jpeg"),
                ])


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


class TestSplitNodesLinks(unittest.TestCase):
    def test_eq(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with additional text."
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_link(old_nodes),
                [
                    TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK,
                             "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK,
                             "https://www.youtube.com/@bootdotdev"),
                    TextNode(" with additional text.", TextType.TEXT),
                ])

    def test_no_links_eq(self) -> None:
        text: str = "This is text with a link to ![boot dev](https://www.boot.dev and ![to youtube](https://www.youtube.com/@bootdotdev)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(split_nodes_link(old_nodes),
                         [TextNode(text, TextType.TEXT)])

    def test_text_first_eq(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_link(old_nodes),
                [
                    TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK,
                             "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK,
                             "https://www.youtube.com/@bootdotdev"),
                ])

    def test_link_first_eq(self) -> None:
        text: str = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_link(old_nodes),
                [
                    TextNode("to boot dev", TextType.LINK,
                             "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK,
                             "https://www.youtube.com/@bootdotdev"),
                ])


class TestSplitNodesImages(unittest.TestCase):
    def test_eq(self) -> None:
        text: str = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) with additional text."
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_image(old_nodes),
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE,
                             "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("obi wan", TextType.IMAGE,
                             "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" with additional text.", TextType.TEXT),
                ])

    def test_no_images_eq(self) -> None:
        text: str = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(split_nodes_image(old_nodes),
                         [TextNode(text, TextType.TEXT)])

    def test_text_first_eq(self) -> None:
        text: str = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_image(old_nodes),
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE,
                             "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("obi wan", TextType.IMAGE,
                             "https://i.imgur.com/fJRm4Vk.jpeg"),
                ])

    def test_image_first_eq(self) -> None:
        text: str = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        old_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
        self.assertEqual(
                split_nodes_image(old_nodes),
                [
                    TextNode("rick roll", TextType.IMAGE,
                             "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("obi wan", TextType.IMAGE,
                             "https://i.imgur.com/fJRm4Vk.jpeg"),
                ])


class TestExtractMarkdown(unittest.TestCase):
    def test_links_eq(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
                extract_markdown_links(text),
                [
                    ("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com/@bootdotdev"),
                ])

    def test_images_eq(self) -> None:
        text: str = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
                extract_markdown_images(text),
                [
                    ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ])

    def test_both_eq(self) -> None:
        text: str = "This is text with a link [to boot dev](https://www.boot.dev) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
                [extract_markdown_links(text), extract_markdown_images(text)],
                [
                    [("to boot dev", "https://www.boot.dev")],
                    [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
                ])
