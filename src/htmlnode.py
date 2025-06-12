class HTMLNode:
  """ Object representing html tags, inline or block
        All params optional:
          no tag -> render as raw text
          no children -> has value (LeafNode)
          no props -> no attributes
          no value -> has children (ParentNode)
  """
  def __init__(self, tag=None, value=None, children=None, props=None):
    """Initialize HTMLNode object

    Args:
        tag (string, optional): html tag like <p>. Defaults to None.
        value (string, optional): content of html tag (tags, text, images...). Defaults to None.
        children (list, optional): list of HTMLNodes objects. Defaults to None.
        props (dictionary, optional): html attributes, where key is name of attribute and value is attribute value/content. Defaults to None.
    """
    self.tag = tag # str (html tag)
    self.value = value # str (html tag content)
    self.children = children # list[HTMLNode] (children html objects)
    self.props = props # dict (html attributes)

  def to_html(self):
    """Convert object HTMLNode into html tag (html syntax) - specific for each object child, children will override this with its own methods
    """
    raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self):
    """Convert props(dict) into html attributes 

    Returns:
        list of strings: list of strings - each string is html attribute ['class="some-class"', ]
    """
    if self.props == None:
      return ""
    attributes = self.props.items() # iterable list[tuple]
    attributes_list = list(map(lambda attribute: f' {attribute[0]}="{attribute[1]}"', attributes)) # list[str]
    return ''.join(attributes_list)
    
  def __repr__(self):
    """Return rext version of object"""
    return f"HTMLNode: ({self.tag}, {self.value}, {self.children}, {self.props})"
