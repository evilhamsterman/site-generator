import re
from enum import StrEnum


class BlockTypes(StrEnum):
    PARAGRAPH: str = "paragraph"
    HEADING: str = "heading"
    CODE: str = "code"
    QUOTE: str = "quote"
    UNORDERED_LIST: str = "unordered_list"
    ORDERED_LIST: str = "orderd_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    blocks = []
    block = ""
    in_block = False
    for line in lines:
        if line != "":
            in_block = True
            block += line + "\n"
        elif in_block and block != "":
            in_block = False
            blocks.append(block.rstrip("\n"))
            block = ""
    if block != "":
        blocks.append(block.rstrip("\n"))
    return blocks


def block_to_block_type(markdown: str) -> BlockTypes:
    lines = markdown.splitlines()
    if len(lines) == 1 and re.match(r"[#]+ [\S]+", lines[0]):
        return BlockTypes.HEADING
    if lines[0] == "```" and lines[-1] == "```":
        return BlockTypes.CODE
    if all(map(lambda x: re.match(r"^>", x), lines)):
        return BlockTypes.QUOTE
    if all(map(lambda x: re.match(r"^[*|-] ", x), lines)):
        return BlockTypes.UNORDERED_LIST
    for i in range(len(lines)):
        if not re.match(f"^{i+1}. ", lines[i]):
            ordered_list = False
            break
        else:
            ordered_list = True

    if ordered_list:
        return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH
