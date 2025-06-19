import os
from document_markdowns import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
  """Takes markdown page, converts it into html and inject template.html page - create index.html

  Args:
      from_path (string): path to markdown file
      template_path (string): path to template.html file
      dest_path (string): destination path, where new index.html file is put
  """
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  with open(from_path, "r") as file:
    markdown = file.read()
  with open(template_path, "r") as file: 
    template = file.read()
  
  html = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)
  content = template.replace("{{ Title }}", title)  
  content = content.replace("{{ Content }}", html)

  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  with open(dest_path, "w") as f:
    f.write(content)
