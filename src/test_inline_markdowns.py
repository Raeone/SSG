import unittest
from textnode import TextType, TextNode
from inline_markdowns import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_bold(self):
    node = [
      TextNode('This is **bold text** in the middle.', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '**', TextType.BOLD) 
    self.assertEqual(len(result), 3)
    self.assertEqual(result[1].text_type, TextType.BOLD)
  
  def test_italic(self):
    node = [
      TextNode('This is _italic text_ in the middle.', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '_', TextType.ITALIC) 
    self.assertEqual(len(result), 3)
    self.assertEqual(result[1].text_type, TextType.ITALIC)
  
  def test_code(self):
    node = [
      TextNode("This is `code` in the middle.", TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, "`", TextType.CODE) 
    self.assertEqual(len(result), 3)
    self.assertEqual(result[1].text_type, TextType.CODE)
  
  def test_bold_at_beginning(self):
    node = [
      TextNode('**Some bold text** at the beginning', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '**', TextType.BOLD) 
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0].text_type, TextType.BOLD)
  
  def test_bold_at_the_end(self):
    node = [
      TextNode('Some text with **bold at the end**', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '**', TextType.BOLD)
    self.assertEqual(len(result), 2)
    self.assertEqual(result[1].text_type, TextType.BOLD)
  
  def test_bold_in_middle_and_end(self):
    node = [
      TextNode('Some text **first bold in middle** and with **second bold at the end**', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '**', TextType.BOLD) 
    self.assertEqual(len(result), 4)
    self.assertEqual(result[1].text_type, TextType.BOLD)
  
  def test_bold_at_beginning_and_end(self):
    node = [
      TextNode('**Some bold text** at the beginning and also **bold end**', TextType.REGULAR)
    ]
    result = split_nodes_delimiter(node, '**', TextType.BOLD) 
    self.assertEqual(len(result), 3)
    self.assertEqual(result[0].text_type, TextType.BOLD)

  def test_bold_on_list_of_nodes(self):
    node = [
      TextNode('This is **bold text** in the middle.', TextType.REGULAR),
      TextNode('This is _italic text_ in the middle.', TextType.REGULAR),
      TextNode('Some text with **bold at the end**', TextType.REGULAR),
      TextNode('Some italic text', TextType.ITALIC)
    ]   
    result = split_nodes_delimiter(node, '**', TextType.BOLD)     
    self.assertEqual(len(result), 7) 
    self.assertEqual(result[0].text_type, TextType.REGULAR)
    self.assertEqual(result[1].text_type, TextType.BOLD)
    self.assertEqual(result[4].text_type, TextType.REGULAR)
    self.assertEqual(result[5].text_type, TextType.BOLD)
    self.assertEqual(result[6].text_type, TextType.ITALIC)
  
  # boot.dev
  def test_delim_bold(self):
    node = TextNode("This is text with a **bolded** word", TextType.REGULAR)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.REGULAR),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word", TextType.REGULAR),
      ],  
      new_nodes,
    )

  def test_delim_bold_double(self):
    node = TextNode(
      "This is text with a **bolded** word and **another**", TextType.REGULAR
      )
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [ 
        TextNode("This is text with a ", TextType.REGULAR),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word and ", TextType.REGULAR),
        TextNode("another", TextType.BOLD),
      ],
        new_nodes,
      )

  def test_delim_bold_multiword(self):
      node = TextNode(
          "This is text with a **bolded word** and **another**", TextType.REGULAR
      )
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      self.assertListEqual(
          [
              TextNode("This is text with a ", TextType.REGULAR),
              TextNode("bolded word", TextType.BOLD),
              TextNode(" and ", TextType.REGULAR),
              TextNode("another", TextType.BOLD),
          ],
          new_nodes,
      )

  def test_delim_italic(self):
      node = TextNode("This is text with an _italic_ word", TextType.REGULAR)
      new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
      self.assertListEqual(
          [
              TextNode("This is text with an ", TextType.REGULAR),
              TextNode("italic", TextType.ITALIC),
              TextNode(" word", TextType.REGULAR),
          ],
          new_nodes,
      )

  def test_delim_bold_and_italic(self):
      node = TextNode("**bold** and _italic_", TextType.REGULAR)
      new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
      new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
      self.assertListEqual(
          [
              TextNode("bold", TextType.BOLD),
              TextNode(" and ", TextType.REGULAR),
              TextNode("italic", TextType.ITALIC),
          ],
          new_nodes,
      )

  def test_delim_code(self):
      node = TextNode("This is text with a `code block` word", TextType.REGULAR)
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
      self.assertListEqual(
          [
              TextNode("This is text with a ", TextType.REGULAR),
              TextNode("code block", TextType.CODE),
              TextNode(" word", TextType.REGULAR),
          ],
          new_nodes,
      )

if __name__ == "__main__":
  unittest.main()
