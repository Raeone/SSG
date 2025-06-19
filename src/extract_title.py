def extract_title(markdown):
  lines = markdown.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[2:]
  raise ValueError("no title found")
