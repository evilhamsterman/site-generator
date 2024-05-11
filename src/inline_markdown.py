import re

from textnode import TextNode, TextTypes


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            nodes.append(node)
            continue
        links = extract_markdown_images(node.text)
        text = node.text
        if len(links) == 0:
            nodes.append(node)
            continue
        for link in links:
            text_parts = text.split(f"![{link[0]}]({link[1]})", 1)
            if len(text_parts) != 2:
                raise ValueError("Invalid Markdown, image not closed")
            if text_parts[0] != "":
                nodes.append(TextNode(text=text_parts[0], text_type=TextTypes.TEXT))
            nodes.append(TextNode(text=link[0], text_type=TextTypes.IMAGE, url=link[1]))
            text = text_parts[1]
        if text != "":
            nodes.append(TextNode(text=text, text_type=TextTypes.TEXT))
    return nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        text = node.text
        if len(links) == 0:
            nodes.append(node)
            continue
        for link in links:
            text_parts = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(text_parts) != 2:
                raise ValueError("Invalid Markdown, link not closed")
            if text_parts[0] != "":
                nodes.append(TextNode(text=text_parts[0], text_type=TextTypes.TEXT))
            nodes.append(TextNode(text=link[0], text_type=TextTypes.LINK, url=link[1]))
            text = text_parts[1]
        if text != "":
            nodes.append(TextNode(text=text, text_type=TextTypes.TEXT))
    return nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes: list[TextNode] = [TextNode(text=text, text_type=TextTypes.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextTypes.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextTypes.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextTypes.CODE)
    return text_nodes
