import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


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
        >> Don't let him in
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
