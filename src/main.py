import argparse

from textnode import TextNode, TextType
from populate_site import *
from generate_page import generate_page_recursive

def main():
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument("basepath", type = str, help="Specify BasePath", default = "/")
    args = parser.parse_args()
    populate_site(SRC, "./docs")
    generate_page_recursive(args.basepath, "./content/", "template.html", "./docs/")
main()
