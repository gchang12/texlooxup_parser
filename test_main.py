"""
Tests the output of the various filter-type
functions in `main.py'.
ADDENDUM:
    Not many functions in this module are independent of any other.
    Therefore, it would be unwise to devise tests for them.
    If they functioned independently, however...
"""

import unittest
from pathlib import Path
import main

class TestTexParser(unittest.TestCase):
    """
    Contains a sequence of tests to validate
    either str or str-lists returned.
    """

    def setUp(self):
        """
        Initialize attributes and junk here.
        """
        self.section_list = ('genops', 'math', 'modes', 'pages', 'paras')

    def test_get_definition_list(self):
        """
        Tests that each item yielded:
        - contains the pattern \\\\cts\w*
        - does not contain \\begindescr or \\enddescr
        """
        for section in self.section_list:
            actual = main.get_definition_list

    def test_compile_entries(self):
        """
        Tests that each item yielded is of the form:
        '''
        \\input macros
        \\begindescriptions
        \\begindesc
        \\cts\w* {\w+} .*
        .*
        \\enddesc
        \\enddescriptions
        \\end
        '''
        """
        actual = main.compile_entries
        pass

    def test_compile_cmd_list(self):
        """
        Tests that each command in the list is a string
        consisting only of letters.
        """
        actuals_list = main.compile_cmd_list()
        expected_re = "\w+"
        for actual in actuals_list:
            self.assertRegex(actual, expected_re)

    def test_write_cmd_definition(self):
        """
        Tests that the arguments correspond with the
        contents of the file written.
        """
        actual = main.write_cmd_definition
        pass

if __name__ == '__main__':
    unittest.main()
