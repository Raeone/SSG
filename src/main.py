import os
import shutil
from copystatic import copy_all_content
from textnode import TextNode, TextType
from leafnode import LeafNode
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
  if os.path.exists(dir_path_public):
    shutil.rmtree(dir_path_public)
  copy_all_content(dir_path_static, dir_path_public)
  generate_page("content/index.md", "template.html", "public/index.html")


main()

