import os

from block_markdown import *
from markdown_to_html import *

def extract_title(markdown: str):
    if os.path.exists(markdown):
        with open(markdown, "r") as f:
            for line in f:
                if line.startswith("# "):
                    line = line.strip("# ")
                    line = line.strip()
                    return line
            raise Exception("Missing required heading")

    else:
        raise Exception("File does not exist")

def generate_page_recursive(basepath, from_path, template_path, dest_path):
    folder_contents = os.listdir(from_path)
    for item in folder_contents:
        if (
            os.path.isfile(os.path.join(from_path, item))
            and item.endswith(".md")
        ):
            generate_page(basepath, os.path.join(from_path, item), template_path, dest_path)
        elif os.path.isdir(os.path.join(from_path, item)):
            generate_page_recursive(basepath, os.path.join(from_path, item), template_path, os.path.join(dest_path, item))

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        source_content = f.read()
    with open(template_path, "r") as t:
        template_content = t.read()
    html_node = markdown_to_html_node(source_content)
    html = html_node.to_html()
    title = extract_title(from_path)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok = True)
    file_name = "".join(from_path.split('/')[-1:])
    file_name = file_name.strip(".md")
    destination_file = os.path.join(dest_path, f"{file_name}.html")
    with open(destination_file, "w") as d:
        d.write(template_content)