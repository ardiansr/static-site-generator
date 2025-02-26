import re

from textnode import TextNode, TextType


def text_to_textnodes(text) -> list[TextNode]:
    text_nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


def split_nodes_delimiter(
        old_nodes: list[TextNode], delimiter: str,
        text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text: str = node.text
        while delimiter in text:
            dlen: int = len(delimiter)
            start: int = text.find(delimiter)
            end: int = text.find(delimiter, start + dlen)
            if end == -1:
                raise ValueError(f"Missing second '{delimiter}' delimiter!")
            if len(text[:start]) > 0:
                new_nodes.append(TextNode(text[:start], TextType.TEXT))
            new_nodes.append(TextNode(text[start + dlen:end], text_type))
            text = text[end + dlen:]
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        text: str = node.text
        links: list[tuple] = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections: list[str] = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[-1]
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        text: str = node.text
        images: list[tuple] = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections: list[str] = text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sections[-1]
        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
