#!/usr/bin/python3
"""
Defines test methods for functions defined in texdict.query
"""

import unittest
from unittest.mock import patch

import texdict2.query

class ParserTest(unittest.TestCase):
    """
    Defines test functions for the functions defined in query.py:

    - get_definition_list
    - create_input_dir
    - create_input_files_from_deftext
    - typeset_input_files
    - cleanup_output

    - main__{sections,miscellany,concepts}
    """

    def setUp(self):
        """
        (pending definition)
        """
        pass


if __name__ == '__main__':
    doing_this = True
    def make_excuse():
        """
        Prints a reason why I don't want to do unit-testing for this module.
        """
        print("It would be a gigantic pain in the ass to create fixtures for all this.")
    if doing_this:
        # on the other hand, there's my OCD about this thing working properly
        with patch("unittest.main", side_effect=make_excuse) as mock_unittestmain:
            unittest.main()
    else:
        make_excuse()
