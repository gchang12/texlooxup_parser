"""
Tests the output of the various filter-type
functions in `main.py'.
ADDENDUM:
    Not many functions in this module are independent of any other.
    Therefore, it would be unwise to devise tests for them.
    If they functioned independently, however...
"""

import unittest
import re
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

    def test_get_definition_text(self):
        """
        Tests that the return value:
        - does not contain the pattern \\(begin|end)descriptions
        - comprises sequences of the pattern [\\a-zA-Z]*\\cts\w* \w+ \{.*\}
        """
        expected_re = "\\\\begindesc([\s.])*[\\\\\w]*\\\\cts\w* [\\\\\w]+ \{.*\}(?=\1*\\\\enddesc)"
        for section in self.section_list:
            actual = main.get_definition_text(Path('sections', section + '.tex').read_text())
            self.assertNotIn("\\begindescriptions", actual)
            self.assertNotIn("\\enddescriptions", actual)
            self.assertGreater(len(re.findall(expected_re, actual)), 1)

    def test_get_definition_list(self):
        """
        Tests that each item yielded:
        - contains the pattern \\\\cts\w*
        - does not contain \\begindescr or \\enddescr
        """
        for section in self.section_list:
            definition_text = main.get_definition_text(Path('sections', section + '.tex').read_text())
            actuals_list = main.get_definition_list(definition_text)
            for actual in actuals_list:
                self.assertNotRegex(actual, "\\\\(begin|end)desc")
                self.assertRegex(actual, "\\\\cts\w*")

    def test_compile_entries(self):
        """
        Tests that each string written to file is of the form:
        '''
        \\input macros
        \\begindescriptions
        \\begindesc
        \\cts\w* {\w+}[\s.]*
        \1*
        \\enddesc
        \\enddescriptions
        \\end
        '''
        """
        expected_re = "\\\\input macros\n\\\\begindescriptions\n\\\\begindesc([\s.])*\\\\cts\w* \{\w+\}(?=\1*\\\\enddesc\n\\\\enddescriptions\n\\\\end)"
        for section in self.section_list:
            index_list = main.compile_entries(section, write_mode=False)
            index_dir = Path('input', section, 'index')
            self.assertTrue(index_dir.exists())
            for index in index_list:
                filename = index_dir.joinpath( str(index) + '.tex' )
                actual = filename.read_text()
                self.assertGreater(len(re.findall(expected_re, actual)), 1)

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
        filename = Path("input", "genops", "index", "62.tex") # a.k.a. "input"
        actual = main.write_cmd_definition(filename, "input", "genops", write_mode=False)
        expected_re = "\\\\cts\w* input .*"
        self.assertRegex(actual, expected_re)

if __name__ == '__main__':
    unittest.main()
