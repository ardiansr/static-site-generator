from enum import Enum
from types import NotImplementedType
from typing import Optional


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
            self, text: str, text_type: TextType,
            url: Optional[str] = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object, /) -> bool | NotImplementedType:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (other.text == self.text and
                other.text_type == self.text_type and
                other.url == self.url)

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
