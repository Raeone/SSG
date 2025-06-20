import os
import shutil
import sys
from copystatic import copy_all_content
from generate_page import generate_pages_recursive

if len(sys.argv) < 2:
  basepath = "/"
basepath = sys.argv[1]

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
  if os.path.exists(dir_path_docs):
    shutil.rmtree(dir_path_docs)
  copy_all_content(dir_path_static, dir_path_docs)
  generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)
  
main()

