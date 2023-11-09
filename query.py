#!/usr/bin/python3
"""
Provides command-line interface to accessing the `TeX for the Impatient' PDF files.
"""

import argparse
from pathlib import Path
import re
import logging
import webbrowser


SECTION_LIST = (
    "concepts",
    "genops",
    "math",
    "miscellany",
    "modes",
    "pages",
    "paras",
    )


def texdict(parser: argparse.ArgumentParser):
    """
    Allows user to look up TeX commands by pattern and section.
    """
    parsed_args = parser.parse_args()
    pattern, sections = (parsed_args.pattern, parsed_args.sections)
    if (pattern, sections) == (None, None) or (pattern, sections) == ("", None):
        # return help message
        parser.parse_args(["-h"])
        return None
    if pattern is None:
        pattern = ".*"
    elif sections is None:
        sections = SECTION_LIST
    # search by section, then by pattern, if any.
    search_results = []
    logging.info("Now searching 'output'/* for sections that are in '%s'.", sections)
    for outdir in Path("output").iterdir():
        if outdir.name not in sections:
            #logging.info("'%s' is not in 'sections' parameter. Skipping.", outdir.name)
            continue
        logging.info("'%s' is in 'sections' parameter. Searching.", outdir.name)
        for outfile in outdir.iterdir():
            if re.search(pattern, outfile.name.replace('.pdf', '')) is None:
                #logging.info("'%s' is not matched by specified 'pattern': '%s'. Skipping.", outfile.name, pattern)
                continue
            logging.info("'%s' is matched by specified 'pattern': '%s'. Appending.", outfile.name, pattern)
            search_results.append("/".join([outdir.name, outfile.name]))
    logging.info("%d results found with pattern='%s', sections='%s'", len(search_results), pattern, sections)
    result_report = "\n    ".join( [
                "",
                f"pattern: '{pattern}'",
                f"sections: {', '.join(sections)}",
                "",
                f"{len(search_results)} results found.",
                ]
            )
    if search_results:
        # print result-set and border
        print(result_report)
        # '.pdf' is trimmed off each list item (-4)
        # the indices are given a minimum width of 3 (+3)
        # the following colon and space are 2 characters (+2)
        border = "=" * (max([len(line) for line in search_results]) - 4 + 5)
        print((" " * 4) + border)
        for index, sresult in enumerate(search_results):
            print((" " * 4) + f"{index:3d}: {sresult.replace('.pdf', '')}")
        # receive user input
        user_input = ""
        while user_input not in [str(index) for index in range(len(search_results))]:
            user_input = input("\n" + (" " * 4) + "Please make a selection: ")
        selection = search_results[int(user_input)]
        print("\n    Now opening PDF: '%s'." % selection)
        webbrowser.open_new(f"output/{selection}")
        print()
        return selection
    else:
        print(result_report)

# TODO: Add in option to specify how to search by pattern (e.g. match, fullmatch, search)
def get_parser():
    """
    Creates an argument parser that has a 'pattern' and a 'sections' attribute.
    """
    parser = argparse.ArgumentParser(
            prog="texdict",
            description="Search for a command to look up by pattern, by section, or by both.",
            epilog="Have a question?\nhttps://github.com/gchang12/texdict2",
        )
    parser.add_argument("-sections",
            metavar="sections",
            type=str,
            nargs="*",
            choices = SECTION_LIST,
            required=False,
            action="extend",
            help="specify which sections to search (default: <all>)",
        )
    parser.add_argument("pattern",
            metavar="pattern",
            type=str,
            nargs="?",
            action="store",
            help="specify the pattern to search for in the list of control sequences (default: .*)",
        )
    return parser

if __name__ == '__main__':
    parser = get_parser()
    texdict(parser)
