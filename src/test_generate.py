import shutil
import unittest
from pathlib import Path, PosixPath
from textwrap import dedent

from generate import TitleNotFoundError, copy_folder, extract_title, replace_placeholder


class TestGenerate(unittest.TestCase):
    def test_copy_folder(self):
        static_path = Path("static")
        public_path = Path("public")
        if public_path.exists():
            shutil.rmtree(public_path)

        expected = [
            (PosixPath("public"), ["images"], ["index.css"]),
            (PosixPath("public/images"), [], ["rivendell.png"]),
        ]
        copy_folder(str(static_path), str(public_path))
        actual = list(public_path.walk())
        self.assertListEqual(expected, actual)

    def test_extract_title(self):
        markdown = dedent(
            """
            # Title

            paragraph
            """
        )
        expected = "Title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_extract_title_not_found(self):
        markdown = dedent(
            """
            Title

            paragraph
            """
        )
        self.assertRaises(TitleNotFoundError, extract_title, markdown)

    def test_replace_placeholder(self):
        template = dedent(
            """
            <html>
                <title> {{ Title }} </title>
            </html>
            """
        )
        expected = template = dedent(
            """
            <html>
                <title> My Title </title>
            </html>
            """
        )
        actual = replace_placeholder(template, "My Title", "{{ Title }}")
        self.assertEqual(expected, actual)
