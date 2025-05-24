import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
