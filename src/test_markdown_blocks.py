import unittest
from textwrap import dedent

from markdown_blocks import BlockTypes, block_to_block_type, markdown_to_blocks


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = dedent(
            """
            This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        )
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",  # noqa: E501
            "* This is a list\n* with items",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)

    def test_markdown_to_blocks_newlines(self):
        markdown = dedent(
            """
            This is **bolded** paragraph




            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        )
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",  # noqa: E501
            "* This is a list\n* with items",
        ]
        actual = markdown_to_blocks(markdown)
        self.assertListEqual(expected, actual)

    def test_block_to_block_type_heading(self):
        block = "# heading"
        expected = BlockTypes.HEADING
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_heading_invalid(self):
        block = dedent(
            """
            # heading
            not heading
        """
        )
        expected = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_code(self):
        block = dedent(
            """\
            ```
            1+2
            ```
            """
        )
        expected = BlockTypes.CODE
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_code_invalid(self):
        block = dedent(
            """\
            ```
            1+2
            """
        )
        expected = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote(self):
        block = dedent(
            """\
            > this
            > is
            > quotes\
            """
        )
        expected = BlockTypes.QUOTE
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote_invalid(self):
        block = dedent(
            """\
            > this
            > is
            > quotes

            """
        )
        expected = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_unordered_list(self):
        blocks = [
            dedent(
                """\
            * list
            * with
            * stars
            """
            ),
            dedent(
                """\
            - list
            - with
            - lines
            """
            ),
        ]
        expected = BlockTypes.UNORDERD_LIST
        for list_type in blocks:
            actual = block_to_block_type(list_type)
            self.assertEqual(expected, actual)

    def test_block_to_block_type_unordered_list_invalid(self):
        blocks = [
            dedent(
                """\
            * list
            * with
            * stars
            not
            """
            ),
            dedent(
                """\
            - list
            - with
            - lines
            not
            """
            ),
        ]
        expected = BlockTypes.PARAGRAPH
        for list_type in blocks:
            actual = block_to_block_type(list_type)
            self.assertEqual(expected, actual)

    def test_block_to_block_type_ordered_list(self):
        block = dedent(
            """\
            1. this
            2. is
            3. list
            """
        )
        expected = BlockTypes.ORDERED_LIST
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = dedent(
            """\
            1. this
            4. is
            3. list
            """
        )
        expected = BlockTypes.PARAGRAPH
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
