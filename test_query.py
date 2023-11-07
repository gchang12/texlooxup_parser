#!/usr/bin/python3
"""
Defines functions that are meant to test the query.texdict function.
"""

from typing import List
import dataclasses
import logging
import unittest

import query

@dataclasses.dataclass
class MockParser:
    """
    """
    pattern: str
    sections: List[str]

    def parse_args(self, args=None, namespace=None):
        """
        """
        pass

class TexdictTest(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        parser: to be tested for certain properties to be expected of it.
        mock_parser: to be passed to query.texdict for testing purposes
        """
        self.parser = query.get_parser()
        self.mock_parser = MockParser("", [])

    def test_get_parser(self):
        """
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:texdict2:%(message)s")
    unittest.main()
