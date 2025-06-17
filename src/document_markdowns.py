from inline_markdowns import text_to_textnodes  
from textnode import text_node_to_html_node
from parentnode import ParentNode
from textnode import TextNode, TextType
from block_markdowns import (
  block_to_block_type,
  markdown_to_blocks,
  BlockType
)

def markdown_to_html_node(markdown): 
  """Final function to put all together. It takes markdkown text and divides it into block of text. For each block it creates HTMLNode object and for content it generate children HTMLNode objects. 
  Returns one final <div> tag with all content. 

  Args:
      markdown (string): markdown document

  Returns:
      HTMLNode: structure of html nodes (converted markdown document)
  """
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html(block) 
    children.append(html_node)
  return ParentNode("div", children, None)

def block_to_html(block):  
  """Helper function for markdown_to_html_node. It takes block of text, finds out its block_type and returns HTMLNode object structure (with children), based on block type. 

  Args:
      block (string): block of markdown text

  Returns:
      HTMLNode: html structure representing md document
  """
  block_type = block_to_block_type(block)
  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html(block)  
  if block_type == BlockType.HEADING:    
    return heading_to_html(block)          
  if block_type == BlockType.CODE:
    return code_to_html(block)    
  if block_type == BlockType.QUOTE:
    return quote_to_html(block)
  if block_type == BlockType.UNORDERED_LIST:
    return ulist_to_html(block)
  if block_type == BlockType.ORDERED_LIST:
    return olist_to_html(block)

def olist_to_html(block):
  """Helper for block_to_html fn. Converts ordered list (md) to HTMLNode structure.

  Args:
      block (string): markdown text

  Returns:
      HTMLNode
  """
  items = []
  lines = block.splitlines()
  for line in lines: 
    text = line[3:]
    children = text_to_children(text)
    items.append(ParentNode("li", children))     
  return ParentNode("ol", items)

def ulist_to_html(block):
  """Helper. Converts unordered list (md) into HTMLNode structure objects. 

  Args:
      block (string)

  Returns:
      HTMLNode
  """
  items = []
  lines = block.splitlines() 
  for line in lines:
    text = line.lstrip("- ").strip()
    children = text_to_children(text)
    items.append(ParentNode("li", children))
  return ParentNode("ul", items)

def quote_to_html(block):
  """Helper. Converts blockquote md text into HTMLNode objects structure.

  Args:
      block (string): 

  Raises:
      ValueError: if not starting with ">" not a blockquote

  Returns:
      HTMLNode: 
  """
  line_content = [] # ["line content", ]
  lines = block.splitlines() # ['>line', ]
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    line_content.append(line.lstrip(">").strip()) # "content of line"
  content = " ".join(line_content)    
  children = text_to_children(content)
  return ParentNode("blockquote", children)

def code_to_html(block):
  """Helper. Convert code (md) into HTMLNodes

  Args:
      block (string): 

  Raises:
      ValueError: 

  Returns:
      HTMLNode: 
  """
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")
  text = block[4:-3]
  raw_text_node = TextNode(text, TextType.REGULAR)
  child = text_node_to_html_node(raw_text_node)
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])

def paragraph_to_html(block):
  """Helper. Convert paragraph text (md) into html object structure. 

  Args:
      block (string): 

  Returns:
      ParentNode: 
  """
  lines = block.splitlines()
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)

def heading_to_html(block):
  """Helper. Converts md heading into html nodes structure

  Args:
      block (string): 

  Returns:
      HTMLNode: 
  """
  heading_hashes, content = block.split(maxsplit=1)    # ['###', 'content']  
  tag = heading_html(heading_hashes)    
  children = text_to_children(content)              
  return ParentNode(tag, children)

def heading_html(heading_hashes):
  """Helper for heading_to_html. Count number of # and returns appropriate tag <h1>, <h2> ...

  Args:
      heading_hashes (string): string of "###"

  Raises:
      ValueError: invalid num of #

  Returns:
      string: "h1", "h2", ...
  """
  match len(heading_hashes):
    case 1:
      return "h1"
    case 2: 
      return "h2"
    case 3: 
      return "h3"
    case 4:
      return "h4"
    case 5: 
      return "h5"
    case 6: 
      return "h6"
    case _: 
      raise ValueError("Invalid heading")

def text_to_children(text):
  """Helper. Takes text, and convert into html objects structure

  Args:
      text (string): md text

  Returns:
      HTMLNode: 
  """
  text_nodes = text_to_textnodes(text) # list of TextNodes  
  children = []
  for node in text_nodes:    
    children.append(text_node_to_html_node(node))
  return children # list of LeafNodes
