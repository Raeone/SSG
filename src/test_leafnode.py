import unittest
from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a(self):
    node = LeafNode("a", "Some link", {"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Some link</a>')
  
  def test_leaf_to_html_no_tag(self):
    node = LeafNode(None, "Hello world!")
    self.assertEqual(node.to_html(), "Hello world!")

  def test_missing_required_argument_tag(self):
      self.assertRaises(TypeError, LeafNode)
      
  if __name__ == "__main__":
    unittest.main()
    