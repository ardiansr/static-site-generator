from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], delimiter: str,
        text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text: str = node.text
            while delimiter in text:
                dlen: int = len(delimiter)
                start: int = text.find(delimiter)
                end: int = text.find(delimiter, start + dlen)
                if end == -1:
                    raise ValueError(
                            f"Missing second '{delimiter}' delimiter!")
                if len(text[:start]) > 0:
                    new_nodes.append(TextNode(text[:start], TextType.TEXT))
                new_nodes.append(TextNode(text[start + dlen:end], text_type))
                text = text[end + dlen:]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
