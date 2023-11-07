#!/usr/bin/python3
"""
Defines functions to extract data from `TeX for the Impatient' source.

1. Given a section, compile a list of definitions that are in that section.
2. Create a directory to store files for this section.
3. For each definition, create named input file for the commands present.
4. Log and inspect invalid command names as necessary.
"""

import logging
import re
import os
from pathlib import Path

KERNEL_FILES = ("config", "eplain", "fonts", "macros")


def get_definition_list(section: str):
    """
    Retrieves list of definitions delimited by \\enddesc and \\begindesc.
    """
    logging.info("parser.get_definition_list('%s')", section)
    filetext = Path("impatient").joinpath(section + ".tex").read_text()
    deflist = []
    for index, rawtext in enumerate(re.split("\\\\begindesc[^r]", filetext)):
        if not index:
            continue
        deftext = re.split("\\\\enddesc[^r]", rawtext)
        deflist.append(deftext[0])
    logging.info("%d definitions were found in '%s' section.", len(deflist), section)
    return deflist

def create_input_dir(section: str):
    """
    Creates a folder for the input files for a given section.
    """
    Path("input", section).mkdir(parents=True, exist_ok=True)
    logging.info("input/'%s' directory created.", section)
    for file in KERNEL_FILES:
        intext = Path("impatient").joinpath(file + ".tex").read_text()
        Path("input", section, file + ".tex").write_text(intext)

def create_input_files_from_deftext(deftext: str, section: str):
    """
    Creates input files from a given definition-text.
    """
    ifile_head = ["\\input macros", "\\begindescriptions", "\\begindesc"]
    ifile_tail = ["\\enddesc", "\\enddescriptions", "\\end"]
    exceptions = {
            'paras': {'/': "_forwardslash"},
            'modes': {},
            'genops': {},
            'math': {},
            'pages': {},
            }
    for line in deftext.splitlines():
        search_result = re.search("\\\\cts\w* (\S+)", line)
        if search_result is None:
            continue
        try:
            filename = search_result.group(1)
            if filename in exceptions[section]:
                filename = exceptions[section][filename]
        except IndexError:
            continue
        logging.info("Found '%s/%s' control sequence. Writing.", section, filename)
        if re.fullmatch("[a-zA-Z]+", filename) is None:
            logging.warning("'%s/%s' is not a valid filename. Please inspect.", section, filename)
        ifile_text = "\n".join( ifile_head + deftext.splitlines() + ifile_tail)
        try:
            Path("input", section, filename + ".tex").write_text(ifile_text)
        except PermissionError:
            logging.warning("PermissionError. '%s/%s' not written.", section, filename)
            break

def typeset_input_files(section: str):
    """
    Typesets all input files created in previous step.
    """
    logging.info("cd input/%s.", section)
    os.chdir(f"input/{section}")
    output_dir = Path("..", "..", "output", section)
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("input/%s directory created.", section)
    ifile_list = list(Path().glob("*.tex"))
    num_files = len(ifile_list)
    logging.info("%d files found. Now processing.", num_files)
    for filenum, filename in enumerate(ifile_list, start=1):
        jobname = filename.name.replace(".tex", "")
        if jobname in KERNEL_FILES:
            logging.info("Skipping kernel file: '%s'.", filename.name)
            continue
        logging.info("Processing file #%d of %d: '%s/%s'", filenum, num_files, section, filename.name)
        os.system(f"pdftex -jobname {jobname} -output-directory {str(output_dir)} {str(filename)}")

def cleanup_output(section: str):
    """
    Clears all non-PDF files from output directory.
    """
    for miscfile in Path("output", section).iterdir():
        if ".pdf" in miscfile.name:
            continue
        logging.info("Removing '%s'.", miscfile.name)
        miscfile.unlink()

if __name__ == '__main__':
    section = "pages"
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:texdict2:%(message)s", filename="log_texdict2.log")
    """
    create_input_dir(section)
    for deftext in get_definition_list(section):
        create_input_files_from_deftext(deftext, section)
    """
    #typeset_input_files(section)
    cleanup_output(section)
