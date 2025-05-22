from enum import Enum

# Python enum for TextNode type
class TextType(Enum):
  NORMAL = "normal"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMG = "img"

# Represent inline text and it's form (bold, italic, etc.)
class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
    
  # Compare 2 text nodes
  def __eq__(self, other):
    return (
      self.text == other.text
      and self.text_type == other.text_type 
      and self.url == other.url
    )
  
  # Return string representation of text node
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
