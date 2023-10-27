#!/usr/bin/python3
"""
"""

import re
from pathlib import Path


def get_parsed_section(filename):
    """
    """
    filetext = Path("impatient").joinpath(filename).read_text()
    linelist = []
    for index, rawtext in enumerate(re.split("\\\\begindesc[^r]", filetext)):
        if not index:
            continue
        deftext = re.split("\\\\enddesc[^r]", rawtext)
        linelist.append(deftext[0])
    return linelist

if __name__ == '__main__':
    linelist = get_parsed_section("math.tex")
