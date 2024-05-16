from enum import StrEnum, auto

from htmlnode import LeafNode


class TextTypes(StrEnum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


class TextNode:
    def __init__(self, text: str, text_type: TextTypes, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: "TextNode") -> bool:
        if (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode('{self.text}', '{self.text_type}', '{self.url}')"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextTypes.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextTypes.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextTypes.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextTypes.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextTypes.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextTypes.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text},
        )
    else:
        raise ValueError(f"Invalid text type {text_node.text_type}")
