import os, stat
import shutil

from block_markdown import *
from config import SRC, DEST
from htmlnode import *
from inline_markdown import *
from markdown_to_html import *

def populate_site(root_src: str = SRC, root_dest: str = DEST) -> list[str] | str:
    copied_files = []
    if os.path.exists(root_src):
        if os.path.exists(root_dest):
            shutil.rmtree(root_dest, True)
            print(f"Removed existing directory: {root_dest}")
        os.mkdir(root_dest)
        return copy_files_to_public(root_src, root_dest, copied_files)
    raise Exception(f"Folder {root_src} does not exist!")

def copy_files_to_public(src, dest, copied_files) -> list[str]:
    folder_contents = os.listdir(src)
    for item in folder_contents:
        if os.path.isfile(os.path.join(src, item)):
            if not os.path.exists(dest):
                os.mkdir(dest)
            shutil.copy(os.path.join(src, item), dest)
            copied_files.append(os.path.join(src, item))
        elif os.path.isdir(os.path.join(src, item)):
            copy_files_to_public(os.path.join(src, item), os.path.join(dest, item), copied_files)
    return copied_files