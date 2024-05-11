import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class Test_HTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com"})
        expected = ' href="https://google.com"'
        actual = node.props_to_html()
        self.assertEqual(expected, actual)


class Test_LeafNode(unittest.TestCase):
    def test_to_html_raw(self):
        value = "regular text"
        node = LeafNode(tag=None, value=value)
        expected = value
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_no_props(self):
        value = "tagged"
        node = LeafNode(value=value, tag="b")
        expected = f"<b>{value}</b>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_with_props(self):
        value = "props"
        node = LeafNode(value=value, tag="a", props={"href": "https://google.com"})
        expected = f'<a href="https://google.com">{value}</a>'
        actual = node.to_html()
        self.assertEqual(expected, actual)


class Test_ParentNode(unittest.TestCase):
    children: list = [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ]

    def test_basic_to_html(self):
        node = ParentNode(tag="p", children=self.children)

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

    def test_empty_tag(self):
        node = ParentNode(tag=None, children=self.children)
        self.assertRaises(ValueError, node.to_html)

    def test_empty_children(self):
        node = ParentNode(tag="b", children=None)  # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_nested_parent(self):
        children = self.children + [ParentNode(tag="span", children=self.children)]
        node = ParentNode(tag="p", children=children)
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<span><b>Bold text</b>Normal text<i>italic text</i>Normal text</span></p>"  # noqa E501
        actual = node.to_html()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
