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
    print(blocks)
