import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is an unequal txt node", TextType.BOLD)
        node2 = TextNode("This is an unequal text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is matching text", TextType.ITALIC)
        node2 = TextNode("This is matching text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is matching text", TextType.BOLD, "https://dccyber.co.uk")
        node2 = TextNode("This is matching text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_no_eq_all(self):
        node = TextNode("This is non-matching text", TextType.BOLD, "https://dccyber.co.uk")
        node2 = TextNode("This is matching text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

 
    # def test_TextType_property(self):
    #    node = TextNode("This is a text node", TextType.ITALIC)
    #    self.assertTrue(self.text_type.BOLD in TextType)



if __name__ == '__main__':
    unittest.main()