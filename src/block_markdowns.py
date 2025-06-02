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
