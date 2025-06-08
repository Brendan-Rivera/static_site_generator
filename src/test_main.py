import unittest

from main import extract_title

class TestMain(unittest.TestCase):

    
    def test_valid_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_whitespace(self):
        self.assertEqual(extract_title("   #    Welcome to Markdown    "), "Welcome to Markdown")

    def test_multiple_lines(self):
        markdown = "## Subtitle\n# Actual Title\nSome more text"
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_title_not_first_line(self):
        markdown = "\n\n## Something\n\n# Title after spacing"
        self.assertEqual(extract_title(markdown), "Title after spacing")

    def test_no_h1_header(self):
        markdown = "## Subtitle only\nSome text\n### Another"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_h1_not_properly_spaced(self):
        markdown = "#TitleWithoutSpace"
        with self.assertRaises(ValueError):
            extract_title(markdown)