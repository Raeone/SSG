import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
  def test_extract_title(self):
    title = "# Some title"
    result = extract_title(title)
    self.assertEqual(result, "Some title")
  
  def test_extract_title_more_lines(self):
    title = """# Some title
some lines
lines"""
    result = extract_title(title)
    self.assertEqual(result, "Some title")

if __name__ == "__main__":
  unittest.main()
