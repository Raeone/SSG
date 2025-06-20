import os
from document_markdowns import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
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
  content = content.replace('href="/', f'href="{base_path}')
  content = content.replace('src="/', f'src="{base_path}')

  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  with open(dest_path, "w") as f:
    f.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
  directory = os.listdir(dir_path_content) # [file, dir, ...]
  print(directory)
  for item in directory:
    print(f"..checking {item} ")
    item_path = os.path.join(dir_path_content, item)
    if os.path.isfile(item_path):
      print(f"item is file {item}")
      name = os.path.splitext(item)[0]  # "about.md" → "about"
      dest_path = os.path.join(dest_dir_path, name + ".html")
      print(f"item path: {item_path} and dest_path {dest_path}")
      generate_page(item_path, template_path, dest_path, base_path)
    else:
      dest_path = os.path.join(dest_dir_path, item)
      print(f"item is directory {item}")
      generate_pages_recursive(item_path, template_path, dest_path, base_path)

