#!/usr/bin/python3
"""
Defines functions to extract, parse, and process data from `TeX for the Impatient' source.

GETTING DEFINITIONS FROM SECTIONS
=================================
1. Given a section, compile a list of definitions that are in that section.
2. Create a directory to store files for this section.
3. For each definition, create named input file for the commands present.
4. Log and inspect invalid command names as necessary.

CREATING OUTPUT FILES
=====================
i.      Create input directory.
ii.     Generate input files.
iii.    Create output directory.
iv.     Typeset.
v.      Clean up output directory.
"""

from typing import List
import logging
import re
import os
from pathlib import Path


AUX_FILES = ("config", "eplain", "fonts", "macros")


def get_definition_list(section: str) -> List[str]:
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
    Creates a folder for the input files for a given section, and inserts the needed files.

    Needed files, per AUX_FILES tuple: config, eplain, fonts, macro
    """
    Path("input", section).mkdir(parents=True, exist_ok=True)
    logging.info("'input/%s' directory created.", section)
    for file in AUX_FILES:
        intext = Path("impatient").joinpath(file + ".tex").read_text()
        Path("input", section, file + ".tex").write_text(intext)
    logging.info("input/{%s,%s,%s,%s} files created", *AUX_FILES)

def create_input_files_from_deftext(deftext: str, section: str):
    """
    Creates input files from a given definition-text from a section.

    Allows user to give input to invalid filenames, and skip them if necessary.
    """
    ifile_head = ["\\input macros", "\\begindescriptions", "\\begindesc"]
    ifile_tail = ["\\enddesc", "\\enddescriptions", "\\end"]
    renamed_command_list = []
    for line in deftext.splitlines():
        search_result = re.search("\\\\cts\w* (\S+)", line)
        if search_result is None:
            continue
        try:
            filename = search_result.group(1)
        except IndexError:
            continue
        logging.info("Found '%s/%s' control sequence.", section, filename)
        if re.fullmatch("[a-zA-Z]+", filename) is None:
            old_filename = filename
            print(deftext)
            print("A filename is invalid if it appears in the list of renamed commands:", [cmd[1:] for cmd in renamed_command_list])
            while (re.fullmatch("[a-zA-Z]+", filename) is None) or ("_" + filename in renamed_command_list):
                filename = input(f"'{section}/{filename}.tex' is not a valid filename. Please either input 'SKIP' to skip this file, or input a filename of the form: [a-zA-Z]+\n\n")
            if filename == "SKIP":
                logging.warning("Discarding '%s/%s'.", section, old_filename)
                continue
            # to denote that this was a filename that needed amending
            filename = "_" + filename
            logging.info("Renamed '%s/%s' to '%s/%s'.", section, old_filename, section, filename)
            renamed_command_list.append(filename)
        ifile_text = "\n".join( ifile_head + deftext.splitlines() + ifile_tail)
        logging.info("Attempting to write '%s/%s'.", section, filename)
        Path("input", section, filename + ".tex").write_text(ifile_text)
        logging.info("Successfully written '%s/%s'.", section, filename)

def typeset_input_files(section: str):
    """
    Typesets all input files in 'input/{section}', and moves the output into 'output/{section}'.
    """
    logging.info("cd input/%s.", section)
    os.chdir(f"input/{section}")
    output_dir = Path("..", "..", "output", section)
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("'input/%s' directory created.", section)
    ifile_list = list(Path().glob("*.tex"))
    num_files = len(ifile_list)
    logging.info("%d files found. Now processing.", num_files)
    for filenum, filename in enumerate(ifile_list, start=1):
        jobname = filename.name.replace(".tex", "")
        if jobname in AUX_FILES:
            logging.info("Skipping auxiliary file: '%s'.", filename.name)
            continue
        logging.info("Processing file #%d of %d: '%s/%s'", filenum, num_files, section, filename.name)
        os.system(f"pdftex -jobname {jobname} -output-directory {str(output_dir)} -interaction batchmode {str(filename)} > /dev/null")
    os.chdir("../..")

def cleanup_output(section: str):
    """
    Clears all non-PDF files from output directory.
    """
    for miscfile in Path("output", section).iterdir():
        if ".pdf" in miscfile.name:
            continue
        logging.info("Removing '%s'.", miscfile.name)
        miscfile.unlink()

def main__sections():
    """
    Creates output for the sections: genops, math, modes, pages, paras.

    1. Creates an input directory to store the source files.
    2. Creates the source files.
    3. Creates an output directory for each section.
    4. Typesets the files.
    5. Cleans up non-PDF files.
    """
    logging.info("Running: main__sections()")
    section_list = ("genops", "math", "modes", "pages", "paras")
    logging.info("Now creating filesystem for sections: %s", section_list)
    for section in section_list:
        create_input_dir(section)
        for deftext in get_definition_list(section):
            create_input_files_from_deftext(deftext, section)
        typeset_input_files(section)
        cleanup_output(section)

def main__miscellany():
    """
    Creates output for the sections: capsule, errors, examples, tips, usebook, usermacs, usingtex

    Stored in 'miscellany' output directory.
    """
    logging.info("Running: main__miscellany()")
    miscellany_list = ("usebook", "usingtex", "examples", "tips", "errors", "usermacs", "capsule")
    output_dir = "miscellany"
    create_input_dir(output_dir)
    output_path = Path("output", output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logging.info("'%s' directory created", str(output_path))
    # examples.tex references xmptext.tex
    logging.info("'%s' needed for 'examples.tex. Copying.", "impatient/xmptext.tex")
    example_text = Path("impatient", "xmptext.tex").read_text()
    output_path.joinpath("xmptext.tex").write_text(example_text)
    logging.info("'%s' successfully written from '%s'.", str(output_path.joinpath("xmptext.tex")), "impatient/xmptext.tex")
    for miscellany in miscellany_list:
        itext = Path("impatient", miscellany + ".tex").read_text()
        Path("input", "miscellany", miscellany + ".tex").write_text(itext)
    typeset_input_files(output_dir)
    cleanup_output(output_dir)

def main__concepts():
    """
    Creates output for the 'concepts' section.

    Stored in 'concepts' output directory.
    """
    logging.info("Running: main__concepts()")
    logging.info("reading 'impatient/concepts.tex' to memory.")
    itext = Path("impatient", "concepts.tex").read_text()
    concept_defs = re.split(r"\\concept\W+", itext)[1:]
    output_dir = "concepts"
    create_input_dir(output_dir)
    output_path = Path("output", output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logging.info("'%s' directory created.", str(output_path))
    ctrlseq_names = ("anatomy", "plainTeX", "TeXMeX")
    ifile_head = ["\\input macros", "\\beginconcepts"]
    ifile_tail = ["\\endconcepts", "\\end"]
    for concept_def in concept_defs:
        concept_name = concept_def.splitlines()[0].strip()
        # for exceptional names encountered
        if concept_name[:-1] in ctrlseq_names:
            concept_def = "\\" + concept_def
        # for spaced names, and special names.
        if concept_name[-1] == "}":
            concept_def = "{" + concept_def
        concept_def = "\\concept " + concept_def.replace("\\pagebreak", "")
        concept_def = re.sub(r"\\conceptindex.*$", "", concept_def)
        concept_lines = ifile_head + concept_def.splitlines() + ifile_tail
        concept_name = re.sub("\W", "", concept_name).replace(" ", "-")
        Path("input", "concepts").joinpath(concept_name + ".tex").write_text("\n".join(concept_lines))
        logging.info("'input/concepts/%s.tex' written to disk.", concept_name)
    typeset_input_files(output_dir)
    cleanup_output(output_dir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:texdict2:%(message)s", filename="log_texdict2.log")
    output_dirlist = ("paras", "miscellany", "concepts")
    output_factories = (main__sections, main__miscellany, main__concepts)
    for outdir, outfunc in zip(output_dirlist, output_factories):
        if Path("output", outdir).exists():
            logging.info("'output/%s' exists. Assuming that '%s' has already been run. Skipping.", outdir, outfunc.__name__)
            continue
        outfunc()
