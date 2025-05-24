import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def setUp(self):
    self.node = HTMLNode('a', "Some link", None, { "href": "https://www.google.com", "target": "_blank",})
  
  def test_to_html(self):
    self.assertRaises(NotImplementedError, self.node.to_html)

  def test_props_to_html(self):
    self.assertEqual(' href="https://www.google.com" target="_blank"', self.node.props_to_html())

  def test_values(self):
        self.assertEqual(
            self.node.tag,
            "a",
        )
        self.assertEqual(
            self.node.value,
            "Some link",
        )
        self.assertEqual(
            self.node.children,
            None,
        )
        self.assertEqual(
            self.node.props,
            { "href": "https://www.google.com", "target": "_blank"}
        )
    
  def test_repr(self):
    expected = """HTMLNode
 tag: a
 content: Some link
 children: None
 attributes: [('href', 'https://www.google.com'), ('target', '_blank')]"""
    self.assertEqual(repr(self.node), expected)
