import unittest

from block_markdown import *
from textnode import TextNode, TextType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here, plus an extra preceding blank line
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here, plus an extra preceding blank line\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_whitespace(self):
        md = """
This is **bolded** paragraph with five extra whitespace characters ->     

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph with five extra whitespace characters ->",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_h1(self):
        md = "# This is a block of type Heading 1"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h2(self):
        md = "## This is a block of type Heading 2"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h3(self):
        md = "### This is a block of type Heading 3"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h4(self):
        md = "#### This is a block of type Heading 4"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h5(self):
        md = "##### This is a block of type Heading 5"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h6(self):
        md = "###### This is a block of type Heading 6"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h7(self):
        md = "####### This is a block of type Heading 7 (non-existant)"
        blocktype = block_to_blocktype(md)
        self.assertNotEqual(blocktype, BlockType.HEADING)

    def test_block_to_blocktype_h7_paragraph(self):
        md = "####### This is a block of type Heading 7 (non-existant)"
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        md = """
```
Code block
```
"""
        md = markdown_to_blocks(md)
        blocktype = block_to_blocktype(md[0])
        self.assertEqual(blocktype, BlockType.CODE)

    def test_block_to_blocktype_code_unbalanced_backticks(self):
        md = """
```
Code block
``
"""
        md = markdown_to_blocks(md)
        blocktype = block_to_blocktype(md[0])
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_blocktype_quote(self):
        md = """
>Quote block line 1
>Quote block line 2
> Quote block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_block_to_blocktype_quote_line_unquoted(self):
        md = """
>Quote block line 1
>Quote block line 2
Quote block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_blocktype_unordered_list(self):
        md = """
- Unordered list block line 1
- Unordered list block line 2
- Unordered list block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_unordered_list_missing_dash(self):
        md = """
- Unordered list block line 1
- Unordered list block line 2
Unordered list block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list(self):
        md = """
1. Ordered list block line 1
2. Ordered list block line 2
3. Ordered list block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_block_to_blocktype_ordered_list_missing_number(self):
        md = """
1. Ordered list block line 1
2. Ordered list block line 2
Ordered list block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_not_starting_from_1(self):
        md = """
2. Ordered list block line 1
3. Ordered list block line 2
4. Ordered list block line 3
"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

if __name__ == '__main__':
     unittest.main()