"""
"""

from typing import (
    Any,
    List,
    Iterable,
)
import re
import shutil
from pathlib import Path

from texlooxup_parser._logging import logger

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
    match = re.search("{(.+?)}", first_line)
    if match is None:
        return None
    return match.group(1)

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
    pattern = r"\\cts[a-z]* ([^ ]+?) "
    # search for line containing '\cts'
    cts_names = re.findall(pattern, filetext)
    return cts_names

def extract_cts_lines(filetext: str) -> Iterable[str]:
    """
    """
    pattern = r"\\cts[a-z]* ([^ ]+?) "
    # search for line containing '\cts'
    filelines = filetext.splitlines()
    cts_lines = filter(lambda line: re.search(pattern, line) is not None, filelines)
    return cts_lines

def _is_cts_line(line: str) -> bool:
    """
    """
    pattern = r"\\cts[a-z]* ([^ ]+?) "
    match = re.search(pattern, line)
    return match is not None

def extract_titled_descriptions(filetext: str, cts_lines: List[str]) -> List[str]:
    """
    """
    titled_descriptions = []
    filelines = filetext.splitlines()
    for cts_line in cts_lines:
        titled_filelines = filter(
            lambda line: not _is_cts_line(line) or (_is_cts_line(line) and line == cts_line),
            filelines,
        )
        titled_descriptions.append("\n".join(titled_filelines))
    return titled_descriptions

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
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            cts_lines = extract_cts_lines(filetext)
            for line in cts_lines:
                prefix = line[:line.index(" ")]
                prefixes.add(prefix)
        return prefixes
    #prefixes = compile_cts_prefixes(); print(prefixes)

    def compile_cts_names():
        """
        """
        names = set()
        for chapter in TFTI_CHAPTERS:
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            names.update(extract_cts_names(filetext))
        return names
    #names = compile_cts_names(); print(names)

    def make_section_subdirectories():
        """
        """
        logger.debug("Now creating subdirectories in '%s'.", TARGET_DIR)
        write_report = {}
        for chapter in TFTI_CHAPTERS:
            output_dir = Path(TARGET_DIR, chapter)
            output_dir.mkdir(exist_ok=True, parents=True)
            write_report[chapter] = 1
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            sections = split_sections(filetext)
            for section in sections:
                section_name = extract_title(section)
                if section_name is None:
                    continue
                output_dir.joinpath(section_name).mkdir(exist_ok=True, parents=True)
                write_report[chapter] += 1
        logger.info("Directory creation successful. Report: %r", write_report)

    def cleanup():
        """
        """
        logger.debug("The '%s' directory has been removed.", TARGET_DIR)
        shutil.rmtree(TARGET_DIR)

    def generate_section_indices():
        """
        """
        logger.debug("Populating directories in '%s'.", TARGET_DIR)
        write_report = {}
        for chapter in TFTI_CHAPTERS:
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            sections = split_sections(filetext)
            section = sections[0]
            output_dir = Path(TARGET_DIR, chapter)
            output_file = output_dir.joinpath("_index.tex")
            bytes_written = output_file.write_text(section, encoding="utf-8")
            if bytes_written == 0:
                logger.warning("Index file for '%s' is empty.", output_dir)
            write_report[chapter] = bytes_written
        logger.info("Index files have been generated. %r", write_report)

    def populate_section_subdirectories():
        """
        """
        logger.debug("Populating directories in '%s'.", TARGET_DIR)
        # \chapter...
        for chapter in TFTI_CHAPTERS:
            filetext = Path(SOURCE_DIR, chapter + ".tex").read_text(encoding="utf-8")
            logger.debug("Populating the '%s' directory.", chapter)
            write_report = {}
            sections = split_sections(filetext)
            # \section...
            for index_no, section in enumerate(sections[1:]):
                section_name = extract_title(section)
                write_report[section_name] = []
                if section_name is None:
                    output_dir = Path(TARGET_DIR, chapter)
                else:
                    output_dir = Path(TARGET_DIR, chapter, section_name)
                subsections = split_subsections(section)
                # \subsection...
                for subsection in subsections:
                    descriptions = split_descriptions(subsection)
                    # \begindesc...\enddesc
                    for description in descriptions:
                        cts_lines = extract_cts_lines(description)
                        titled_descriptions = extract_titled_descriptions(description, cts_lines)
                        for titled_desc in titled_descriptions:
                            cts_name = extract_cts_names(titled_desc).pop().replace("/", "_SOLIDUS_")
                            output_file = output_dir.joinpath(cts_name + ".tex")
                            instance_no = 1
                            while output_file.exists():
                                instance_no += 1
                                output_file = output_dir.joinpath(cts_name + "%d.tex" % instance_no)
                            bytes_written = output_file.write_text(titled_desc, encoding="utf-8")
                            if bytes_written == 0:
                                logger.warning("Article file '%s' is empty.", output_file)
                            write_report[section_name].append((output_file.name.replace('.tex', ''), bytes_written))
            logger.info("Write report for '%s': %r", chapter, write_report)

    def split_docs():
        """
        """
        cleanup()
        make_section_subdirectories()
        populate_section_subdirectories()

    split_docs()
