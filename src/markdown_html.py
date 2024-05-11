import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockTypes, block_to_block_type, markdown_to_blocks
from textnode import text_node_to_html_node


def children_to_html(text: str) -> list[HTMLNode]:
    html_nodes: list[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    result: list[HTMLNode] = []

    # Parse markdown into blocks
    blocks = markdown_to_blocks(markdown=markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        # Quote blocks
        if block_type == BlockTypes.QUOTE:
            html_nodes: list[HTMLNode] = []
            for line in block.splitlines():
                html_nodes.extend(children_to_html(line.lstrip("> ")))
            result.append(ParentNode(tag="blockquote", children=html_nodes))

        # Unordered List blocks
        elif block_type == BlockTypes.UNORDERD_LIST:
            html_nodes: list[HTMLNode] = []
            for line in block.splitlines():
                line_text = re.sub(r"^[*|-] ", "", line)
                html_nodes.append(
                    ParentNode(tag="li", children=children_to_html(line_text))
                )
            result.append(ParentNode(tag="ul", children=html_nodes))

        # Ordered List
        elif block_type == BlockTypes.ORDERED_LIST:
            html_nodes: list[HTMLNode] = []
            for line in block.splitlines():
                line_text = re.sub(r"^^[\d]+. ", "", line)
                html_nodes.append(
                    ParentNode(tag="li", children=children_to_html(line_text))
                )
            result.append(ParentNode(tag="ol", children=html_nodes))

        # Code
        elif block_type == BlockTypes.CODE:
            block = re.sub(r"\n*```\n*", "", block)
            code = LeafNode(tag="code", value=block)
            result.append(ParentNode(tag="pre", children=[code]))

        # Headings
        elif block_type == BlockTypes.HEADING:
            levels = block.find(" ")
            line_text = block[levels + 1 :]
            result.append(
                ParentNode(tag=f"h{levels}", children=children_to_html(line_text))
            )

        # Everything else is a paragraph
        else:
            text = block.replace("\n", " ").rstrip()
            result.append(ParentNode(tag="p", children=children_to_html(text)))

    return ParentNode("div", result)
