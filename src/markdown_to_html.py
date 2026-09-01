from block_markdown import *
from htmlnode import *
from inline_markdown import *
from textnode import *

def markdown_to_html_node(markdown: str):
    html_nodes: list[HTMLNode] = []
    div_node = ParentNode("div", html_nodes) # type: ignore # Top-level node. All block nodes should be children in the html_nodes list. This may need to go at the end.
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_blocktype(block)
        if blocktype == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            child_text_nodes = text_to_children(block)
            if len(child_text_nodes) == 1:
                node = LeafNode("p", block)
            node = ParentNode("p", child_text_nodes)
            html_nodes.append(node)
        if blocktype == BlockType.HEADING:
            header_type = heading_type(block)
            block = block.strip('# ')
            child_heading_nodes = text_to_children(block)
            if len(child_heading_nodes) == 1:
                node = LeafNode(f"h{header_type}", block)
            node = ParentNode(f"h{header_type}", child_heading_nodes)
            html_nodes.append(node)
        if blocktype == BlockType.QUOTE:
            new_block = []
            block = block.splitlines()
            for line in block:
                line = line.replace("> ", "")
                new_block.append(line)
            new_block = " ".join(new_block)
            quote_children = text_to_children(new_block)
            node = ParentNode("blockquote", quote_children)
            html_nodes.append(node)
        if blocktype == BlockType.UNORDERED_LIST:
            unordered_list_children = []
            block = unordered_list_format(block)
            for item in block:
                item = LeafNode("li", item)
                unordered_list_children.append(item)
            node = ParentNode("ul", unordered_list_children)
            html_nodes.append(node)
        if blocktype == BlockType.ORDERED_LIST:
            ordered_list_children = []
            block = ordered_list_format(block)
            ordered_list_children.extend(list_item_nodes(block))
            node = ParentNode("ol", ordered_list_children)
            html_nodes.append(node)
        if blocktype == BlockType.CODE:
            code_block_children = []
            block = code_format(block)
            code_block = TextNode(block, TextType.CODE)
            code_block_children.append(text_node_to_html_node(code_block))
            code_parent = ParentNode("pre", code_block_children)
            html_nodes.append(code_parent)
    return div_node

def text_to_children(text: str):
    child_nodes = text_to_textnodes(text)
    child_html_nodes = []
    for node in child_nodes:
        child_html_nodes.append(text_node_to_html_node(node))
    return child_html_nodes
        

def heading_type(block: str) -> int | None:
    if block.startswith("# "):
        return 1
    if block.startswith("## "):
        return 2
    if block.startswith("### "):
        return 3
    if block.startswith("#### "):
        return 4
    if block.startswith("##### "):
        return 5
    if block.startswith("###### "):
        return 6

def unordered_list_format(text):
    list_items = text.splitlines(text)
    stripped_items = []
    for item in list_items:
        item = item.strip("- ")
        stripped_items.append(item.strip("\n"))
    return stripped_items

def ordered_list_format(text):
    new_ordered_list = []
    stripped_items = text.splitlines()
    for count, item in enumerate(stripped_items, start = 1):
        item = item.strip(f"{count}. ")
        new_ordered_list.append(item)
    return new_ordered_list

def list_item_nodes(block_list):
    children = []
    for item in block_list:
        item = LeafNode("li", item)
        children.append(item)
    return children

def code_format(code):
    code = code.strip("```\n")
    code = code.strip("```")
    return code