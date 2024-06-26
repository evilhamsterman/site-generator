import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextTypes


class TestInlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_links(self):
        links = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"  # noqa: E501
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        actual = extract_markdown_links(links)
        self.assertEqual(expected, actual)

    def test_extract_markdown_images(self):
        images = "This is text with an ![image](https://example.com/image1.png) and ![another](https://example.com/image2.jpg)"  # noqa: E501
        expected = [
            ("image", "https://example.com/image1.png"),
            ("another", "https://example.com/image2.jpg"),
        ]
        actual = extract_markdown_images(images)
        self.assertEqual(expected, actual)

    def test_split_nodes_images(self):
        images = TextNode(
            "This is text with an ![image](https://example.com/image1.png) and ![another](https://example.com/image2.jpg)",  # noqa: E501
            TextTypes.TEXT,
        )
        expected = [
            TextNode("This is text with an ", TextTypes.TEXT),
            TextNode("image", TextTypes.IMAGE, "https://example.com/image1.png"),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("another", TextTypes.IMAGE, "https://example.com/image2.jpg"),
        ]
        actual = split_nodes_image([images])
        self.assertListEqual(expected, actual)

    def test_split_nodes_links(self):
        images = TextNode(
            "This is text with a [link](https://example.com) and [another](https://google.com)",  # noqa: E501
            TextTypes.TEXT,
        )
        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "https://example.com"),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("another", TextTypes.LINK, "https://google.com"),
        ]
        actual = split_nodes_link([images])
        self.assertListEqual(expected, actual)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"  # noqa: E501
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("text", TextTypes.BOLD),
            TextNode(" with an ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" word and a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" and an ", TextTypes.TEXT),
            TextNode(
                "image",
                TextTypes.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",  # noqa: E501
            ),
            TextNode(" and a ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
