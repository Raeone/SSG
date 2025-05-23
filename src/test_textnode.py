import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is also a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.BOLD, None)
        node5 = TextNode("This is a text node", TextType.BOLD, None) 
        node6 = TextNode("This is a text node", TextType.REGULAR)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertEqual(node4, node5)
        self.assertNotEqual(node, node6)
    
    def test_repr(self):
        node = TextNode("Some node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(Some node, bold, None)")


if __name__ == "__main__":
    unittest.main()
    