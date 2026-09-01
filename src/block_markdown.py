from enum import Enum

from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    sections = markdown.split("\n\n")
    for block in sections:
        if block != "":
            blocks.append(block.strip())
    return blocks

def block_to_blocktype(block: str) -> BlockType:
    if (
        block.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### '),)
    ):
        return BlockType.HEADING
    else:
        sections = block.splitlines()
        new_list = []
        for line in sections:
            if line != "":
                new_list.append(line)
        if (
                len(sections) > 1
                and sections[0].startswith('```')
                and sections[-1].endswith('```')
            ):
                return BlockType.CODE
        if all(lines.startswith('>') for lines in new_list):
            return BlockType.QUOTE
        if all(lines.startswith('- ') for lines in new_list):
            return BlockType.UNORDERED_LIST
        else:
            ordered_list = True
            for count, line in enumerate(new_list, start = 1):
                if line.startswith(str(count)+'.'):
                    ordered_list = True
                else:
                    ordered_list = False
                    break
            if ordered_list:
                return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH