#!/usr/bin/python3
"""
Defines functions that are meant to test the query.texdict function.
"""

from typing import List, Any
import logging
import unittest
from unittest.mock import patch

import query

class MockParser:
    """
    """

    def __init__(self, pattern: str, sections: List[str], called_with: List[Any] = []):
        self.pattern = pattern
        self.sections = sections
        self.called_with = []

    def parse_args(self, args=None, namespace=None):
        """
        """
        self.called_with.append((args, namespace))
        return self

class TexdictTest(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        parser: to be tested for certain properties to be expected of it.
        mock_parser: to be passed to query.texdict for testing purposes
        """
        self.parser = query.get_parser()
        self.mock_parser = MockParser(None, None)

    def test_get_parser(self):
        """
        Tests that 'sections' and 'pattern' parameters are created for parser.
        """
        self.assertEqual(self.parser.prog, "texdict")
        logging.info("parser has name: texdict")
        parsed_args = self.parser.parse_args(["para", "-sections", "paras", "pages"])
        arg_attrs = ("pattern", "sections")
        arg_types = (str, list)
        for attrtype, attrname in zip(arg_types, arg_attrs):
            self.assertTrue(hasattr(parsed_args, attrname))
            attrval = getattr(parsed_args, attrname)
            self.assertIsInstance(attrval, attrtype)
            logging.info("parser has '%s' attr of type '%s': '%s'", attrname, attrtype, attrval)
        # attrval is parsed_args.sections as of last iteration of loop
        logging.info("checking that get_parser().sections is a subset of (query.SECTION_LIST := %s)", query.SECTION_LIST)
        for index, section in enumerate(attrval):
            self.assertIsInstance(section, str)
            self.assertIn(section, query.SECTION_LIST)
            logging.info("(parser.sections[%d] := '%s') in query.SECTION_LIST", index, section)
        parsed_args = self.parser.parse_args(["para", "-sections", "paras", "genops"])
        self.assertEqual(parsed_args.pattern, "para")
        self.assertEqual(parsed_args.sections, ['paras', 'genops'])

    @patch("__main__.input")
    def test_texdict(self, mockinput):
        """
        Tests functionality of 'texdict' function.
        """
        pdfopener_name = "webbrowser.open_new"
        mockinput.return_value = "0"
        # 1: both pattern and sections are None 
        none = query.texdict(self.mock_parser)
        self.assertEqual(len(self.mock_parser.called_with), 2)
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertIn((["-h"], None), self.mock_parser.called_with)
        self.mock_parser.called_with.clear()
        # 2: sections is None
        self.mock_parser.sections = None
        self.mock_parser.pattern = "par"
        with patch(pdfopener_name) as mock_pdfopener:
            selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 3: pattern is None
        self.mock_parser.sections = ["genops", "paras"]
        self.mock_parser.pattern = None
        with patch(pdfopener_name) as mock_pdfopener:
            selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 4: neither sections nor pattern is None
        self.mock_parser.sections = ["genops", "paras"]
        self.mock_parser.pattern = "par"
        with patch(pdfopener_name) as mock_pdfopener:
            selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 5: pattern not found
        self.mock_parser.sections = ["genops"]
        self.mock_parser.pattern = "^$"
        with patch(pdfopener_name) as mock_pdfopener:
            none = query.texdict(self.mock_parser)
        self.assertIsNone(none)
        mock_pdfopener.assert_not_called()
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:texdict2:%(message)s")
    unittest.main()
