#!/usr/bin/python3
"""
"""

from pathlib import Path

import pypandoc

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/excerpts/"
PATH_TO_MACROS = "./input/impatient/macros.tex"

def decorate_input_text(filetext: str, path_to_macros: Path | str = PATH_TO_MACROS) -> str:
    """
    """
    filelines = filetext.splitlines()
    decorated_filelines = \
        ["\\begindescriptions", "\\begindesc"] \
        + filelines \
        + ["\\enddesc", "\\enddescriptions", "\\end"]
    macro_text = Path(path_to_macros).read_text(encoding="utf-8") + "\n"
    return \
        macro_text \
        + "\n".join(decorated_filelines) \
        .replace("\\input macros.tex", macro_text)

def convert_tex_to_html(filetext: str):
    """
    """
    html_text = pypandoc.convert_text(filetext, format="tex", to="html")
    return html_text

if __name__ == "__main__":
    #filetext = Path("input", "impatient", "pages.tex").read_text(encoding="utf-8")
    filetext = Path(SOURCE_DIR, "genops", "Registers", "advance.tex").read_text(encoding="utf-8")
    print("filetext:", filetext)
    decorated_filetext = decorate_input_text(filetext)
    #print("decorated_filetext:", decorated_filetext)
    html_text = convert_tex_to_html(decorated_filetext)
    print("html_text:", html_text)
