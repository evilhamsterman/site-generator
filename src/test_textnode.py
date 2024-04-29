import unittest

from src import textnode
from textnode import TextNode, TextTypes, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_split_nodes(self):
        node = TextNode(
            text="This is text with a `code block` word", text_type=TextTypes.TEXT
        )
        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT),
        ]
        actual = split_nodes_delimiter([node], "`", text_type=TextTypes.CODE)
        self.assertListEqual(expected, actual)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode(
                text="This is text with a `code block` word", text_type=TextTypes.TEXT
            ),
            TextNode(text="This is a `code` word", text_type=TextTypes.TEXT),
        ]
        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT),
            TextNode("This is a ", TextTypes.TEXT),
            TextNode("code", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT),
        ]
        actual = split_nodes_delimiter(nodes, delimiter="`", text_type=TextTypes.CODE)
        self.assertListEqual(expected, actual)

    def test_delimiter_at_end(self):
        node = TextNode(text="word **bold**", text_type=TextTypes.TEXT)
        expected = [
            TextNode("word ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
        ]
        actual = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertListEqual(expected, actual)

    def test_multiple_same_type(self):
        node = TextNode(
            text="This has **multiple** words **bold**", text_type=TextTypes.TEXT
        )
        expected = [
            TextNode("This has ", TextTypes.TEXT),
            TextNode("multiple", TextTypes.BOLD),
            TextNode(" words ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
        ]
        actual = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        self.assertListEqual(expected, actual)

    def test_split_different_types(self):
        node = TextNode(
            text="This has **multiple** `types` of delimiter", text_type=TextTypes.TEXT
        )
        expected = [
            TextNode("This has ", TextTypes.TEXT),
            TextNode("multiple", TextTypes.BOLD),
            TextNode(" `types` of delimiter", TextTypes.TEXT),
        ]
        actual = split_nodes_delimiter([node], delimiter="**", text_type=TextTypes.BOLD)
        self.assertListEqual(expected, actual)

    def test_unclosed_tag(self):
        node = TextNode(text="This **tag is not closed", text_type=TextTypes.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", text_type=TextTypes.BOLD)


if __name__ == "__main__":
    unittest.main()
