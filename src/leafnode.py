from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  """Object representing html tags with no children (just value)

  Args :
      HTMLNode (HTMLNode object)
  """
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
  
  def to_html(self):
    """Render html tag (string) with attribute from object

    Returns:
        string: html tag with attributes as string, ie. "<b>bold</bold>" 
    """
    if self.value is None:
      raise ValueError("All leaf nodes must have a value")
    
    if not self.tag:
      return self.value
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
