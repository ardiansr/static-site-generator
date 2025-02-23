from typing import Optional, Self


class HTMLNode:
    def __init__(
            self,
            tag: Optional[str] = None,
            value: Optional[str] = None,
            children: Optional[list[Self]] = None,
            props: Optional[dict] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return (f"HTMLNode({self.tag}, {self.value},"
                + f" {self.children}, {self.props})")

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        attributes: str = ""
        if self.props == None:
            return attributes
        for key, value in self.props.items():
            attributes += f" {key}=\"{value}\""
        return attributes


class LeafNode(HTMLNode):
    def __init__(
            self, tag: Optional[str], value: str,
            props: Optional[dict] = None) -> None:
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have a value!")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
