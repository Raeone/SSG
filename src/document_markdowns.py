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
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html(block) 
    children.append(html_node)
  return ParentNode("div", children, None)

def block_to_html(block):  
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
  items = []
  lines = block.splitlines()
  for line in lines: 
    text = line[3:]
    children = text_to_children(text)
    items.append(ParentNode("li", children))     
  return ParentNode("ol", items)

def ulist_to_html(block):
  items = []
  lines = block.splitlines() 
  for line in lines:
    text = line.lstrip("- ").strip()
    children = text_to_children(text)
    items.append(ParentNode("li", children))
  return ParentNode("ul", items)

def quote_to_html(block):
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
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")
  text = block[4:-3]
  raw_text_node = TextNode(text, TextType.REGULAR)
  child = text_node_to_html_node(raw_text_node)
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])

def paragraph_to_html(block):
  lines = block.splitlines()
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)

def heading_to_html(block):
  heading_hashes, content = block.split(maxsplit=1)    # ['###', 'content']  
  tag = heading_html(heading_hashes)    
  children = text_to_children(content)              
  return ParentNode(tag, children)

def heading_html(heading_hashes):
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
  text_nodes = text_to_textnodes(text) # list of TextNodes  
  children = []
  for node in text_nodes:    
    children.append(text_node_to_html_node(node))
  return children # list of LeafNodes
