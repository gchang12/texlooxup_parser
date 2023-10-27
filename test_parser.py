#!/usr/bin/python3
"""
"""

import unittest
from unittest.mock import patch

from parser import get_parsed_section


class ParserTest(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.texfile = r"""
        \begindescriptions
        \begindesc
        A-B-C.
        \enddesc
        miscellaneous text
        \begindesc
        Easy as 1-2-3.
        \enddesc
        \enddescriptions
        """

    def test_parse_tftifile(self):
        """
        """
        with self.assertRaises(FileNotFoundError):
            parse_file("???")
        with patch("pathlib.Path.read_text") as mock_text:
            mock_text.return_value = self.texfile
            linelist = get_parsed_section("")
            self.assertEqual(len(linelist), 2)
            self.assertEqual(linelist[0].strip(), "A-B-C.")
            self.assertEqual(linelist[1].strip(), "Easy as 1-2-3.")

if __name__ == '__main__':
    unittest.main()
