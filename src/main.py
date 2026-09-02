from textnode import TextNode, TextType
from populate_site import *
from generate_page import generate_page_recursive

def main():
    populate_site(SRC, DEST)
    generate_page_recursive("./content/", "template.html", "./public/")
main()
