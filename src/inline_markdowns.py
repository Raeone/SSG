import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  """ Extract bold, inline and code blocks of text from TextNodes into new TextNodes with corresponding TextType

  Args:
      old_nodes (list): list of TextNode objects
      delimiter (str): symbol for bold **, italic _, code ` 
      text_type (list): list of TestNode objects with corresponding TextType

  Raises:
      Exception: if no closing delimiter

  Returns:
      list of TextNodes 
  """
  # List of new nodes containing just bold, italic or code text and TextType
  new_nodes = []

  for node in old_nodes:
    # If TextType bold, italic or code, skip, just add to new_nodes
    if node.text_type != TextType.REGULAR:
      new_nodes.append(node)
      continue
    
    # Split TextNode text
    parts = node.text.split(delimiter)

    # Split textnode must have odd items, otherwise there is closing delimiter missing
    if len(parts) % 2 == 0:
      raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}' in '{node.text}'")

    # Append to new_nodes from split textnode - "" is delimiter, skip, odd are our special text_type (bold, italic, code), even are regular text
    for i, part in enumerate(parts):
      if part == "":
        continue
      if i % 2 == 0:
        new_nodes.append(TextNode(part, TextType.REGULAR))
      else:
        new_nodes.append(TextNode(part, text_type))

  return new_nodes


def extract_markdown_images(text): 
  """Extract alt text and url from markdwon image link

  Args:
      text (str): raw markdown text

  Returns:
      list: list of tuples [(alt, url)]
  """
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)  

def extract_markdown_links(text):
  """Extract link text and url from markdown text

  Args:
      text (string): markdown raw text string

  Returns:
      list of tuples: each tuple contains link text and url [(link, url)]
  """
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes): # list of TextNodes(text, text_type, url) -> new list of TextNodes (text_type corresponding)
  """Takes TextNodes and split them into regular TextNodes and image TextNodes

  Args:
      old_nodes (list of TextNodes)

  Returns:
      list of TextNodes: list of regular and image nodes with respective text types
  """
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.REGULAR:
      new_nodes.append(node)
      continue
      
    text_img_node = node.text
    images = extract_markdown_images(text_img_node) # [(alt, url)]
    if not images:
      new_nodes.append(node)
      continue

    for alt, url in images:      
      
      sections = text_img_node.split(f"![{alt}]({url})", 1)
      if len(sections) != 2:
        raise ValueError("invalid markdown, image section not closed")
      
      before, text_img_node = sections
      if before:
        new_nodes.append(TextNode(before, TextType.REGULAR))
      new_nodes.append(TextNode(alt, TextType.IMAGE, url))    
    
    if text_img_node:
      new_nodes.append(TextNode(text_img_node, TextType.REGULAR))
  
  return new_nodes

def split_nodes_link(old_nodes): 
  """Takes TextNodes and split them into regular TextNodes and link TextNodes with respetive text type

  Args:
      old_nodes (list of TextNodes): [TextNodes]

  Returns:
      list of TextNodes: returns list of regular and link text nodes with respective text types
  """
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.REGULAR:
      new_nodes.append(node)
      continue
      
    text_link_node = node.text
    links = extract_markdown_links(text_link_node) # [(link, url)]
    if not links:
      new_nodes.append(node)
      continue
    

    for link, url in links:      
      sections = text_link_node.split(f"[{link}]({url})", 1) 
      if len(sections) != 2:
        raise ValueError("invalid markdown, link section not closed")
      
      before, text_link_node = sections
      if before:
        new_nodes.append(TextNode(before, TextType.REGULAR))
      new_nodes.append(TextNode(link, TextType.LINK, url))    
    
    if text_link_node:
      new_nodes.append(TextNode(text_link_node, TextType.REGULAR))
  
  return new_nodes

def text_to_textnodes(text):
  """Takes text with markdown and split it to TextNodes objects with respective TextType

  Args:
      text (string): markdown text

  Returns:
      list of TextNodes
  """
  nodes = [TextNode(text, TextType.REGULAR)]
  split_img = split_nodes_image(nodes)
  split_link = split_nodes_link(split_img)
  split_code = split_nodes_delimiter(split_link, "`", TextType.CODE)
  split_italic = split_nodes_delimiter(split_code, "_", TextType.ITALIC)
  split_bold = split_nodes_delimiter(split_italic, "**", TextType.BOLD)
  return split_bold
