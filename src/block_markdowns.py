from enum import Enum
# import re

class BlockType(Enum):
  
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown): # string -> list of str
  """Takes raw text in markdown and split it into list of strings, where each string is a block separated with \n\n (empty line)

  Args:
      markdown (string): markdown raw string (whole document)

  Returns:
      list: list of strings, where each string is a block 
  """
  block_strings = markdown.split("\n\n")
  block_strings = list(map(lambda s: s.strip(), block_strings))
  block_strings = list(filter(lambda s: s, block_strings))  
  return block_strings

# same as method below, but here it uses regex
  # def block_to_block_type(block): # string -> BlockType(Enum)
  #   if re.match(r"^#{1,6} [^\s].*", block):
  #     return BlockType.HEADING
  #   elif block.startswith("```") and block.endswith("```"):	
  #     return BlockType.CODE
  #   elif re.fullmatch(r"^(>\s?.*\n?)+$", block):
  #     return BlockType.QUOTE
  #   elif re.fullmatch(r"^(-\s.*\n?)+$", block):
  #     return BlockType.UNORDERED_LIST
  #   elif re.fullmatch(r"^(\d+\.\s.*\n?)+$", block):
  #     return BlockType.ORDERED_LIST
  #   else:
  #     return BlockType.PARAGRAPH

def block_to_block_type(block): # str -> BlockType
  """Takes block of text and decide, what type of block (BlockType enum) it is (paragraph, code, quote, list, ...)

  Args:
      block (string): takex block of text

  Returns:
      BlockType: type of block as BlockType.enum
  """
  lines = block.split("\n")

  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return BlockType.HEADING
  if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
    return BlockType.CODE
  if block.startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return BlockType.PARAGRAPH
    return BlockType.QUOTE
  if block.startswith("- "):
    for line in lines:
      if not line.startswith("- "):
        return BlockType.PARAGRAPH
    return BlockType.UNORDERED_LIST
  if block.startswith("1. "):
    i = 1
    for line in lines:
      if not line.startswith(f"{i}. "):
        return BlockType.PARAGRAPH
      i += 1
    return BlockType.ORDERED_LIST
  return BlockType.PARAGRAPH
