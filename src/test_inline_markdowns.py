import unittest
import re
from textnode import TextType, TextNode
from inline_markdowns import (
  split_nodes_delimiter, 
  extract_markdown_images, 
  extract_markdown_links,
  split_nodes_image,
  split_nodes_link,
)

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

class TextExtractMarkdown(unittest.TestCase):
  def test_extract_markdown_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    result = [
      ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
      ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
      ]
    self.assertEqual(extract_markdown_images(text), result)
  
  def test_extract_markdown_links(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    result = [
      ("to boot dev", "https://www.boot.dev"),
      ("to youtube", "https://www.youtube.com/@bootdotdev")
    ]
    self.assertEqual(extract_markdown_links(text), result)

  # boot.dev
  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
      "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
    )
    self.assertListEqual(
      [
        ("link", "https://boot.dev"),
        ("another link", "https://blog.boot.dev"),
      ],
      matches,
    )

class TestSplitNodesImage(unittest.TestCase):  
  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.REGULAR),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )
  
  def test_split_images_more_nodes(self):
    nodes = [
      TextNode(
        "This is regular text node", TextType.REGULAR
      ),    
      TextNode("Bold text", TextType.BOLD),
      TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
      [
        TextNode("This is regular text node", TextType.REGULAR), 
        TextNode("Bold text", TextType.BOLD),
        TextNode("This is text with an ", TextType.REGULAR),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes
    )
  
  def test_split_images_image_at_beginning(self):    
    nodes = [      
      TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
      [        
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes
    )

  def test_split_images_all_images(self):    
    nodes = [      
      TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
      [        
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),        
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes
    )
  
  # boot.dev
  def test_split_image(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
          TextNode("This is text with an ", TextType.REGULAR),
          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
      ],
      new_nodes,
    )

  def test_split_image_single(self):
    node = TextNode(
      "![image](https://www.example.COM/IMAGE.PNG)",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
      ],
      new_nodes,
    )

  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.REGULAR),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )

class TestSplitNodesLink(unittest.TestCase):  
  def test_split_links(self):
    node = TextNode(
      "This is text with an [Link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.REGULAR),
        TextNode("Link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )
  
  def test_split_links_more_nodes(self):
    nodes = [
      TextNode(
        "This is regular text node", TextType.REGULAR
      ),    
      TextNode("Bold text", TextType.BOLD),
      TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual(
      [
        TextNode("This is regular text node", TextType.REGULAR), 
        TextNode("Bold text", TextType.BOLD),
        TextNode("This is text with an ", TextType.REGULAR),
        TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes
    )
  
  def test_split_link_link_at_beginning(self):    
    nodes = [      
      TextNode(
        "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual(
      [        
        TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.REGULAR),
        TextNode(
            "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes
    )

  def test_split_links_all_links(self):    
    nodes = [      
      TextNode(
        "[link](https://i.imgur.com/zjjcJKZ.png) [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.REGULAR
        ),
    ]
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual(
      [        
        TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),        
        TextNode(' ', TextType.REGULAR),
        TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes
    )
  
  # boot.dev
  def test_split_links(self):
    node = TextNode(
      "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
      TextType.REGULAR,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.REGULAR),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        TextNode(" and ", TextType.REGULAR),
        TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
        TextNode(" with text that follows", TextType.REGULAR),
      ],
      new_nodes,
    )


if __name__ == "__main__":
  unittest.main()

