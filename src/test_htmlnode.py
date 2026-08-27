import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType

class TestHTMLNode(unittest.TestCase):
    def test_default_params(self): # Test default paramaters work correctly.
        node = HTMLNode()
        node2 = HTMLNode("p", "Test")
        self.assertNotEqual(node, node2)

    def test_format(self): # Test HTMLNode prints correctly.
        children = []
        props = {"href": "https://dccyber.co.uk", "target": "_blank",}
        child_node = HTMLNode()
        children.append(child_node)
        node = HTMLNode("<li>", "DCCyber", children, props)
        self.assertEqual(node.props_to_html(), ' href="https://dccyber.co.uk" target="_blank"')
        

    def test_format_partial_params(self):
        children = []
        props = {"href": "https://dccyber.co.uk", "target": "_blank",}
        child_node = HTMLNode()
        children.append(child_node)
        node = HTMLNode(None , None ,children, props)
        return

    def test_leaf_to_html_p(self): # Test "p" tag appears correctly.
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_print(self): # Test LeafNode prints as expected when called.
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

    def test_no_value(self): # Test for ValueError
        node = LeafNode("p", None)
        self.assertRaises(ValueError)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )

    def test_multiple_children(self):
        child_node1 = LeafNode("i", "child")
        child_node2 = LeafNode(None, "plain text child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><i>child</i>plain text child</div>"
        )

    def test_no_children(self):
        parent_node = ParentNode("span", [])
        self.assertRaises(ValueError)

    def test_no_tags(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italics(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://dccyber.co.uk")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://dccyber.co.uk"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "internet/spongebob.img")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "", '{"src": "internet/spongebob.img", "alt": "This is an image node"}')

    def test_invalid_text_type(self):
        node = TextNode("This is an invalid node", "Nonsense")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Unknown text type")

if __name__ == '__main__':
     unittest.main()
    