import shutil
import unittest
from pathlib import Path, PosixPath

from generate import copy_folder


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
