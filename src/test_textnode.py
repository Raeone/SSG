import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq_nodes_equal(self):
        node = TextNode("This is a text node", TextType.REGULAR)
        node2 = TextNode("This is a text node", TextType.REGULAR)
        self.assertEqual(node, node2)

    def test_eq_nodes_differ_in_type(self):
        node = TextNode("This is a text node", TextType.REGULAR)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_nodes_differ_in_text(self):
        node = TextNode("This is a text node", TextType.REGULAR)
        node2 = TextNode("This is a text node2", TextType.REGULAR)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.REGULAR, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, regular, https://www.boot.dev)", repr(node)
        )

class TextNodeToHTMLNode(unittest.TestCase):
  def test_text_node_to_html_node_regular(self):
    node = TextNode("This is a text node", TextType.REGULAR)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_text_node_to_html_node_bold(self):
    node = TextNode("bold text", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "bold text")
  
  def test_text_node_to_html_node_italic(self):
    node = TextNode("italic text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "italic text")
  
  def test_text_node_to_html_node_code(self):
    node = TextNode("code text", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "code text")

  def test_text_node_to_html_node_link(self):
    node = TextNode("Link", TextType.LINK, "www.google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "Link")
    self.assertEqual(html_node.props, {"href": "www.google.com"})
    
if __name__ == "__main__":
    unittest.main()
