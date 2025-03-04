import unittest

from htmlnode import HTMLNode
from markdown_blocks import (BlockType, block_to_block_type, extract_title,
                             markdown_to_blocks, markdown_to_html_node)


class TestExtractTitle(unittest.TestCase):
    def test_raise_value_error(self) -> None:
        markdown: str = """
        ## It is not heading 1 title.
        """
        with self.assertRaisesRegex(ValueError, "Heading 1 is not found."):
            extract_title(markdown)

    def test_eq(self) -> None:
        markdown: str = """
        # Heading 1

        ## Heading 2

        ### Heading 3

        #### Heading 4

        ##### Heading 5

        ###### Heading 6
        """
        self.assertEqual(extract_title(markdown), "Heading 1")


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_eq(self) -> None:
        markdown: str = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<p>"
                + "This is <b>bolded</b> paragraph text in a p tag here"
                + "</p>"
                + "<p>"
                + "This is another paragraph with <i>italic</i> text and "
                + "<code>code</code> here"
                + "</p>"
                + "</div>")

    def test_heading_eq(self) -> None:
        markdown: str = """
        # This is bolded paragraph

        ## text in a p

        ### tag here

        #### This is another paragraph with _italic_ text and `code` here

        ####### It's not heading
        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<h1>This is bolded paragraph</h1>"
                + "<h2>text in a p</h2>"
                + "<h3>tag here</h3>"
                + "<h4>"
                + "This is another paragraph with <i>italic</i> text and "
                + "<code>code</code> here"
                + "</h4>"
                + "<p>####### It's not heading</p>"
                + "</div>")

    def test_code_eq(self) -> None:
        markdown: str = """
        ```
        This is text _should_ remain
        the **same** even with inline stuff
        ```
        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<pre>"
                + "<code>"
                + "This is text _should_ remain\nthe **same** "
                + "even with inline stuff"
                + "</code>"
                + "</pre>"
                + "</div>")

    def test_quote_eq(self) -> None:
        markdown: str = """
        > All that glitters is not gold.

        Spongebob Squarepants
        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<blockquote>"
                + "All that glitters is not gold."
                + "</blockquote>"
                + "<p>Spongebob Squarepants</p>"
                + "</div>")

    def test_unordered_list_eq(self) -> None:
        markdown: str = """
        - Don't pick up the call
        - Don't let him in
        - Don't be his friend
        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<ul>"
                + "<li>Don't pick up the call</li>"
                + "<li>Don't let him in</li>"
                + "<li>Don't be his friend</li>"
                + "</ul>"
                + "</div>")

    def test_ordered_list_eq(self) -> None:
        markdown: str = """
        1. Don't pick up the call
        1. Don't let him in
        1. Don't be his friend
        """
        html_node: HTMLNode = markdown_to_html_node(markdown)
        self.assertEqual(
                html_node.to_html(),
                "<div>"
                + "<ol>"
                + "<li>Don't pick up the call</li>"
                + "<li>Don't let him in</li>"
                + "<li>Don't be his friend</li>"
                + "</ol>"
                + "</div>")


class TestBlockToBlockType(unittest.TestCase):
    def test_code_not_eq(self) -> None:
        markdown: str = """
        ```ts
        const add = (a: number, b: number): number => {
          return a + b;
        };
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_not_eq(self) -> None:
        markdown: str = """
        > Don't pick up the call
        - Don't let him in
        > Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_not_eq(self) -> None:
        markdown: str = """
        Don't pick up the call
        - Don't let him in
        - Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_not_eq(self) -> None:
        markdown: str = """
        1. Don't pick up the call
        Don't let him in
        3. Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_eq(self) -> None:
        block: str = "# The Very First Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_eq(self) -> None:
        markdown: str = """
        ```ts
        const add = (a: number, b: number): number => {
          return a + b;
        };
        ```
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_eq(self) -> None:
        markdown: str = """
        > Don't pick up the call
        > Don't let him in
        > Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_eq(self) -> None:
        markdown: str = """
        - Don't pick up the call
        - Don't let him in
        - Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_eq(self) -> None:
        markdown: str = """
        1. Don't pick up the call
        2. Don't let him in
        3. Don't be his friend
        """
        block: str = markdown_to_blocks(markdown)[0]
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_eq(self) -> None:
        markdown: str = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on new line

        - This is a list
        - with items
        """
        self.assertEqual(
                markdown_to_blocks(markdown),
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on new line",
                    "- This is a list\n- with items",
                ])

    def test_no_whitespace_eq(self) -> None:
        markdown: str = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on new line

- This is a list
- with items
        """
        self.assertEqual(
                markdown_to_blocks(markdown),
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on new line",
                    "- This is a list\n- with items",
                ])
