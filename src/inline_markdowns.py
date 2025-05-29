from textnode import TextType, TextNode

# Extract bold, inline and code blocks of text from TextNodes into new TextNodes with corresponding TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
