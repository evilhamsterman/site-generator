import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockTypes, block_to_block_type, markdown_to_blocks
from textnode import text_node_to_html_node


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
                text_nodes = text_to_textnodes(line.lstrip("> "))
                for text_node in text_nodes:
                    html_nodes.append(text_node_to_html_node(text_node))
            result.append(ParentNode(tag="blockquote", children=html_nodes))

        # Unordered List blocks
        elif block_type == BlockTypes.UNORDERD_LIST:
            html_nodes: list[HTMLNode] = []
            for line in block.splitlines():
                line_nodes: list[LeafNode] = []
                text_nodes = text_to_textnodes(re.sub(r"^[*|-] ", "", line))
                for text_node in text_nodes:
                    line_nodes.append(text_node_to_html_node(text_node))
                html_nodes.append(ParentNode(tag="li", children=line_nodes))
            result.append(ParentNode(tag="ul", children=html_nodes))

        # Ordered List
        elif block_type == BlockTypes.ORDERED_LIST:
            html_nodes: list[HTMLNode] = []
            for line in block.splitlines():
                line_nodes: list[LeafNode] = []
                text_nodes = text_to_textnodes(re.sub(r"^^[\d]+. ", "", line))
                for text_node in text_nodes:
                    line_nodes.append(text_node_to_html_node(text_node))
                html_nodes.append(ParentNode(tag="li", children=line_nodes))
            result.append(ParentNode(tag="ol", children=html_nodes))

        # Code
        elif block_type == BlockTypes.CODE:
            block = re.sub(r"\n*```\n*", "", block)
            code = LeafNode(tag="code", value=block)
            result.append(ParentNode(tag="pre", children=[code]))

        # Headings
        elif block_type == BlockTypes.HEADING:
            levels = block.find(" ")
            line_nodes = []
            text_nodes = text_to_textnodes(block[levels + 1 :])
            for text_node in text_nodes:
                line_nodes.append(text_node_to_html_node(text_node))
            result.append(ParentNode(tag=f"h{levels}", children=line_nodes))

        # Everything else is a paragraph
        else:
            html_nodes: list[HTMLNode] = []
            text = block.replace("\n", " ").rstrip()
            text_nodes = text_to_textnodes(text)
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            result.append(ParentNode(tag="p", children=html_nodes))

    return ParentNode("div", result)
