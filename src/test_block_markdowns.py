import unittest
from block_markdowns import (
  markdown_to_blocks,
  block_to_block_type,
  BlockType
)

class TestMarkdownToBlocks(unittest.TestCase):
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

  def test_empty_lines(self):
    md = """
  This is some text.  



  and some text.
  """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks, 
      [
        "This is some text.",
        "and some text."
      ]
    )
  
  def test_stripped_blocks(self):
    md = """
This is some text.    

  and more.   
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is some text.",
        "and more."
      ]
    )

class TestBlockToBlockType(unittest.TestCase):
  def test_heading(self):
    block = "#### Some heading"
    wrong_block = "some text"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    self.assertNotEqual(block_to_block_type(wrong_block), BlockType.HEADING)
  
  def test_code(self):
    code = "```some code\nsome code```"
    not_code = "some text"
    self.assertEqual(block_to_block_type(code), BlockType.CODE)
    self.assertNotEqual(block_to_block_type(not_code), BlockType.CODE) 

  def test_one_line_quote(self):
    quote = "> some quote"
    not_quote = "some text"
    self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
    self.assertNotEqual(block_to_block_type(not_quote), BlockType.QUOTE)
    
  def test_multiline_quote(self):
    quote = """> some quote
> another line of quote"""
    self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

  def test_unordered_list(self):
    list = """- item
- item
- item"""
    not_list = """item
item"""
    self.assertEqual(block_to_block_type(list), BlockType.UNORDERED_LIST)
    self.assertNotEqual(block_to_block_type(not_list), BlockType.UNORDERED_LIST)
  
  def test_ordered_list(self):
    list = """1. item
2. item
3. item"""
    not_list = """item
item"""
    self.assertEqual(block_to_block_type(list), BlockType.ORDERED_LIST)
    self.assertNotEqual(block_to_block_type(not_list), BlockType.ORDERED_LIST)

  # boot.dev
  def test_block_to_block_types(self):
    block = "# heading"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    block = "```\ncode\n```"
    self.assertEqual(block_to_block_type(block), BlockType.CODE)
    block = "> quote\n> more quote"
    self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    block = "- list\n- items"
    self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    block = "1. list\n2. items"
    self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    block = "paragraph"
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__": 
  unittest.main()
