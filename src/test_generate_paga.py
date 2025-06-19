import unittest
from generate_page import *

class TestGeneratePage(unittest.TestCase):
  def test(self):
    generate_page("content/index.md", "template.html", "public")

  
    

if __name__ == "__main__":
  unittest.main()
