import os
import shutil
from copystatic import copy_all_content
from textnode import TextNode, TextType
from leafnode import LeafNode

dir_path_static = "./static"
dir_path_public = "./public"

def main():
  if os.path.exists(dir_path_public):
    shutil.rmtree(dir_path_public)
  copy_all_content(dir_path_static, dir_path_public)

main()
