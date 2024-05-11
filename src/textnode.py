from enum import StrEnum

from htmlnode import LeafNode


class TextTypes(StrEnum):
    TEXT: str = "text"
    BOLD: str = "bold"
    ITALIC: str = "italic"
    CODE: str = "code"
    LINK: str = "link"
    IMAGE: str = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextTypes, url: str = None) -> None:
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

    def __repr__(self) -> str:
        return f"TextNode('{self.text}', '{self.text_type}', '{self.url}')"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextTypes:
        raise ValueError(f"Invalid text type {text_node.text_type}")

    if text_node.text_type == TextTypes.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == TextTypes.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == TextTypes.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == TextTypes.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextTypes.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextTypes.IMAGE:
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
