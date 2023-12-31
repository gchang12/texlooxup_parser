#!/usr/bin/python3
"""
Defines functions that are meant to test the query.texdict function.
"""

import io
from typing import List, Any
import logging
import unittest
from unittest.mock import patch

from texdict2 import query

class MockParser:
    """
    Exists to mock the argparse.ArgumentParser class.
    """

    def __init__(self, pattern: str, sections: List[str], called_with: List[Any] = []):
        """
        pattern: The pattern to search in the list of filenames.
        sections: The list of sections whence to get that list of filenames.
        called_with: Testing purposes only; exists to record the number of calls to 'parse_args'
        """
        self.pattern = pattern
        self.sections = sections
        self.called_with = []

    def parse_args(self, args=None, namespace=None):
        """
        To be pseudo-mocked by 'texdict'. Records what arguments it is called with.
        """
        self.called_with.append((args, namespace))
        return self

class TexdictTest(unittest.TestCase):
    """
    Defines tests for query.{get_parser,texdict} methods.
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

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("webbrowser.open_new")
    @patch("builtins.input")
    def test_texdict(self, mockinput, mock_pdfopener, mock_stdout):
        """
        Tests functionality of 'texdict' function.
        """
        mockinput.return_value = "0"
        # 1: both pattern and sections are None 
        none = query.texdict(self.mock_parser)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.assertIn((None, None), self.mock_parser.called_with)
        self.mock_parser.called_with.clear()
        mock_pdfopener.assert_not_called()
        # 2: sections is None
        self.mock_parser.sections = None
        self.mock_parser.pattern = "par"
        selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        mock_pdfopener.reset_mock()
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 3: pattern is None
        self.mock_parser.sections = ["genops", "paras"]
        self.mock_parser.pattern = None
        selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        mock_pdfopener.reset_mock()
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 4: neither sections nor pattern is None
        self.mock_parser.sections = ["genops", "paras"]
        self.mock_parser.pattern = "par"
        selection = query.texdict(self.mock_parser)
        mock_pdfopener.assert_called_once_with(f"output/{selection}")
        mock_pdfopener.reset_mock()
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()
        # 5: pattern not found
        self.mock_parser.sections = ["genops"]
        self.mock_parser.pattern = "^$"
        none = query.texdict(self.mock_parser)
        self.assertIsNone(none)
        mock_pdfopener.assert_not_called()
        mock_pdfopener.reset_mock()
        self.assertIn((None, None), self.mock_parser.called_with)
        self.assertEqual(len(self.mock_parser.called_with), 1)
        self.mock_parser.called_with.clear()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:texdict2:%(message)s")
    unittest.main()
