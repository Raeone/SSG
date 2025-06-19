import os
import shutil
from copystatic import copy_all_content
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
templatep_path = "./template.html"

def main():
  if os.path.exists(dir_path_public):
    shutil.rmtree(dir_path_public)
  copy_all_content(dir_path_static, dir_path_public)
  generate_page(
    os.path.join(dir_path_content, "index.md"), 
    templatep_path,
    os.path.join(dir_path_public, "index.html")
  )
  
main()

