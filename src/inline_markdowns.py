from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.REGULAR:
      new_nodes.append(node)
      continue

    parts = node.text.split(delimiter)

    if len(parts) % 2 == 0:
      raise Exception(f"Invalid markdown: unmatched delimiter '{delimiter}' in '{node.text}'")

    for i, part in enumerate(parts):
      if part == "":
        continue
      if i % 2 == 0:
        new_nodes.append(TextNode(part, TextType.REGULAR))
      else:
        new_nodes.append(TextNode(part, text_type))

  return new_nodes
