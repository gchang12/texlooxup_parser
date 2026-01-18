#!./.venv-texlooxup_parser/bin/python3
"""
"""

import sys
from pathlib import Path

import pypandoc

try:
    filetext = Path(sys.argv[1]).read_text(encoding="utf-8")
    html_text = pypandoc.convert_text(filetext, format="tex", to="html")
    print("html_text:")
    print(html_text)
except IndexError:
    print("Please input a filename.")
