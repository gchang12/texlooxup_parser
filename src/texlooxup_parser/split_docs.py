"""
"""

from typing import (
    Any,
    List,
)
import re

def _split_text_by_pattern(filetext: str, pattern: str) -> List[str]:
    """
    """
    section_list = re.split(pattern, filetext)
    return [section.rstrip("\n") for section in section_list]

def extract_title(filetext: str) -> str:
    """
    """
    first_line = filetext[:filetext.index("\n")]
    title = re.search("{(.+?)}", first_line).group(1)
    return title

def split_sections(filetext: str) -> List[str]:
    """
    """
    pattern = r"\\section"
    section_list = _split_text_by_pattern(filetext, pattern)
    return section_list

def split_subsections(filetext: str) -> List[str]:
    """
    """
    pattern = r"\\subsection"
    subsection_list = _split_text_by_pattern(filetext, pattern)
    return subsection_list

def split_descriptions(filetext: str) -> List[str]:
    """
    """
    pattern = r"\\begindesc(.+?)\\enddesc"
    descriptions = re.findall(pattern, filetext, flags=re.DOTALL)
    return [description.strip() for description in descriptions]

def extract_cts_names(filetext: str) -> str:
    """
    """
    pattern = r"\\cts ([^ ]+?) "
    # search for line containing '\cts'
    cts_names = re.findall(pattern, filetext)
    return cts_names

if __name__ == "__main__":
    TFTI_CHAPTERS = (
        "genops",
        "math",
        "modes",
        "pages",
        "paras",
    )
