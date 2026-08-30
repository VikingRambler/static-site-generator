import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] =="":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        split_nodes = []
        original_text = node.text
        if len(images) == 0:
            new_nodes.append(node)
        for i in range(len(images)):
            sections = original_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            original_text = sections[1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        split_nodes = []
        sections = []
        original_text = node.text
        if len(links) == 0:
            new_nodes.append(node)
        for i in range(len(links)):
            sections = original_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            original_text = sections[1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes