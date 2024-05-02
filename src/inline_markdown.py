import re

from .textnode import TextNode, TextTypes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextTypes
) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            nodes.append(node)
            continue
        node_parts = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Delimiter {delimiter} not closed")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                node_parts.append(TextNode(parts[i], TextTypes.TEXT))
            else:
                node_parts.append(TextNode(parts[i], text_type))
        nodes.extend(node_parts)
    return nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
