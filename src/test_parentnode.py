import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
  def test_initialization(self):
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )    
    self.assertIsInstance(node, ParentNode)

  def test_to_html_no_tag(self):
    node = ParentNode(None, "hello there")
    self.assertRaises(ValueError, node.to_html)
  
  def test_to_html_no_children(self):
    node = ParentNode("p", None)
    self.assertRaises(ValueError, node.to_html)
  
  def test_to_html_simple_children(self):
    node = ParentNode("div", [
      LeafNode("p", "paragraph"),
      LeafNode("p", "paragraph")
    ])
    self.assertEqual(node.to_html(), "<div><p>paragraph</p><p>paragraph</p></div>")

  def test_to_html_nested_children(self):
    node = ParentNode("div", [
      ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text")
        ]),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ]
    )
    self.assertEqual(node.to_html(), "<div><p><b>Bold text</b>Normal text</p><i>italic text</i>Normal text</div>")

  def test_to_html_with_attr(self):
    node = ParentNode("div", [
      ParentNode("p", [
        LeafNode("a", "Link", {"href": "www.google.com"})
        ]),          
      ],
      {"class": "some-class"}
    )
    self.assertEqual(node.to_html(), '<div class="some-class"><p><a href="www.google.com">Link</a></p></div>')

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

  def test_to_html_many_children(self):
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )
    self.assertEqual(
      node.to_html(),
      "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
    )

  def test_headings(self):
    node = ParentNode(
      "h2",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )
    self.assertEqual(
      node.to_html(),
      "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
    )

if __name__ == "__main__":
  unittest.main()
