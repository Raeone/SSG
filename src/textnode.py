from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
  """Python enum for TextNode type
  """
  REGULAR = "regular"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class TextNode:
  """Object representing inline text
  """
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
    
  # Compare 2 text nodes
  def __eq__(self, other):
    """Compare 2 text nodes

    Args:
        other (TextNode): override eq method to compare, if 2 TextNode objects are same

    Returns:
        boolean
    """
    return (
      self.text == other.text
      and self.text_type == other.text_type 
      and self.url == other.url
    )
  
  def __repr__(self):
    """Return string representation of text ndoe"""
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
  """Converts text node object into html node object LeafNode

  Args:
      text_node (TextNode): TextNode object

  Returns:
      LeafNode 
  """
  match text_node.text_type:
    case TextType.REGULAR:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    case _:
      raise Exception(f"invalid text type: {text_node.text_type}") 