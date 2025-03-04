from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown: str) -> str:
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("# ").rstrip()
    raise ValueError("Heading 1 is not found.")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        if block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        if block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        if block_type == BlockType.UNORDERED_LIST:
            children.append(list_to_html_node(block))
        if block_type == BlockType.ORDERED_LIST:
            children.append(list_to_html_node(block))
    return ParentNode("div", children)


def paragraph_to_html_node(block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    block = block.replace("\n", " ")
    text_nodes: list[TextNode] = text_to_textnodes(block)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    hlen: int = block.find(" ")
    if hlen <= 6:
        block = block[hlen + 1:]
    text_nodes: list[TextNode] = text_to_textnodes(block)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode(f"h{hlen}", children)


def code_to_html_node(block: str) -> HTMLNode:
    block = re.sub(r"(`{3}\w+\n)|(`{3}\n)|(\n`{3})", "", block)
    return ParentNode("pre", [LeafNode("code", block)])


def quote_to_html_node(block: str) -> HTMLNode:
    children: list[HTMLNode] = []
    block = re.sub(r"\n>\n", " ", block)
    block = re.sub(r">\s+", "", block)
    text_nodes: list[TextNode] = text_to_textnodes(block)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return ParentNode("blockquote", children)


def list_to_html_node(block: str) -> HTMLNode:
    tag: str = "ul"
    children: list[HTMLNode] = []
    lines: list[str] = block.split("\n")
    for line in lines:
        grandchildren: list[HTMLNode] = []
        if line.startswith("- "):
            line = line.removeprefix("- ")
        else:
            line = re.sub(r"\d+.\s", "", line)
            tag = "ol"
        text_nodes: list[TextNode] = text_to_textnodes(line)
        for text_node in text_nodes:
            grandchildren.append(text_node_to_html_node(text_node))
        children.append(ParentNode("li", grandchildren))
    return ParentNode(tag, children)


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines: list[str] = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"\d+.\s", line) for line in lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    for block in markdown.split("\n\n"):
        block = re.sub(r"(?=\n)\s+", "\n", block.strip())
        if block:
            blocks.append(block)
    return blocks
