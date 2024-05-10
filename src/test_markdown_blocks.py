import unittest

from markdown import markdown_to_blocks


class TestMarkdown(unittest):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",  # noqa: E501
            "* This is a list\n* with items",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)
