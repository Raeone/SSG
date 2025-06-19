def extract_title(markdown):
  first_line = markdown.split("\n")[0]
  
  if not first_line.startswith("# "):
    raise Exception("no title")
  
  return first_line.lstrip("# ").strip()
