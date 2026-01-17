"""
"""

from typing import (
    Any,
    List,
    Iterable,
)
import re
from pathlib import Path

SOURCE_DIR = "./input/impatient/"
TARGET_DIR = "./output/raw-excerpts/"

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

def extract_cts_names(filetext: str) -> List[str]:
    """
    """
    pattern = r"\\cts ([^ ]+?) "
    # search for line containing '\cts'
    cts_names = re.findall(pattern, filetext)
    return cts_names

def extract_cts_lines(filetext: str) -> Iterable[str]:
    """
    """
    pattern = r"\\cts ([^ ]+?) "
    # search for line containing '\cts'
    filelines = filetext.splitlines()
    cts_lines = filter(lambda line: re.search(pattern, line) is not None, filelines)
    return cts_lines

def is_cts_line(line: str) -> bool:
    """
    """
    pattern = r"\\cts ([^ ]+?) "
    match = re.search(pattern, line)
    return match is not None

def get_cts_name(line: str) -> bool:
    """
    """
    pattern = r"\\cts ([^ ]+?) "
    match = re.search(pattern, line)
    return match.group(1)

def get_subsection_name(filetext: str) -> str| None:
    """
    """
    first_line = filetext.splitlines()[0]
    pattern = " {(.+?)}"
    subsection_match = re.fullmatch(pattern, first_line)
    if subsection_match is None:
        return None
    return subsection_match.group(1)

if __name__ == "__main__":
    TFTI_CHAPTERS = (
        "genops",
        "math",
        "modes",
        "pages",
        "paras",
    )
    def compile_cts_prefixes():
        """
        """
        prefixes = set()
        for chapter in TFTI_CHAPTERS:
            filename = SOURCE_DIR + chapter + ".tex"
            filetext = Path(filename).read_text(encoding="utf-8")
            cts_lines = extract_cts_lines(filetext)
            for line in cts_lines:
                prefix = line[:line.index(" ")]
                prefixes.add(prefix)
        return prefixes
    #prefixes = compile_cts_prefixes()
    #print(prefixes)
    def compile_cts_names():
        """
        """
        names = set()
        for chapter in TFTI_CHAPTERS:
            filename = SOURCE_DIR + chapter + ".tex"
            filetext = Path(filename).read_text(encoding="utf-8")
            cts_lines = extract_cts_lines(filetext)
            for line in cts_lines:
                name = get_cts_name(line)
                names.add(name)
        return names
    #names = compile_cts_names()
    #print(names, len(names))
    def make_subsection_subdirectories():
        """
        """
        for chapter in TFTI_CHAPTERS:
            output_dir = Path(TARGET_DIR, chapter)
            output_dir.mkdir(exist_ok=True, parents=True)
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            sections = split_sections(filetext)
            #print("\nChapter: ", chapter)
            #print("=========")
            for subsection in sections:
                subsection_name = get_subsection_name(subsection)
                if subsection_name is None:
                    continue
                output_dir.joinpath(subsection_name).mkdir(exist_ok=True, parents=True)
    make_subsection_subdirectories()
    # for each file:
    # split into sections
    # make new directory for each section
    # for each section, create subsections as necessary
    # for each section, write description
