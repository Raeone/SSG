from htmlnode import HTMLNode

# Object representing html tags with no children (just value)
class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
  
  # Render html tag (string) with attribute from object
  def to_html(self):
    if not self.value:
      raise ValueError("All leaf nodes must have a value")
    
    if not self.tag:
      return self.value
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
