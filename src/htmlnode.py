# Object representing html tags, inline or block
# All params optional:
  # no tag -> render as raw text
  # no value -> has children (ParentNode)
  # no children -> has value (LeafNode)
  # no props -> no attributes
class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag # str (html tag)
    self.value = value # str (html tag content)
    self.children = children # list[HTMLNode] (children html objects)
    self.props = props # dict (html attributes)

  def to_html(self):
    # child classes will override this
    raise NotImplementedError("to_html method not implemented")
  
  # Convert props into html attributes
  def props_to_html(self):
    if self.props == None:
      return ""
    attributes = self.props.items() # iterable list[tuple]
    attributes_list = list(map(lambda attribute: f' {attribute[0]}="{attribute[1]}"', attributes)) # list[str]
    return ''.join(attributes_list)
    
  # Return text version of object  
  def __repr__(self):
    return f"HTMLNode: ({self.tag}, {self.value}, {self.children}, {self.props})"
