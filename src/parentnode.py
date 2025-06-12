from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  """Object representing html tag with no content, but with other html tags (children)

  Args:
      HTMLNode (object)
  """
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)
  
  def to_html(self):
    """Render html tag (string) with nested tags

    Raises:
        ValueError: if no children objects or no tag

    Returns:
        string: html tag and its children as string
    """
    if self.tag is None:
      raise ValueError("invalid HTML: no tag")

    if self.children is None:
      raise ValueError("invalid HTML: no children")

    children_html = ""
    for child in self.children:
      children_html += child.to_html()
    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
