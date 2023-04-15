"""
Reads the `TeX for the Impatient' source files and
outputs them into a format that can be typeset
and consumed easily.
"""

import re
from pathlib import Path
from shutil import rmtree
from logging import getLogger
import logging

logger = getLogger()


def get_definition_text(src_text):
    """
    Retrieves the inner body of a source text.
    """
    definition_text = src_text.split('\\begindescriptions')[-1]
    definition_text = definition_text.split('\\enddescriptions')[0]
    return definition_text


def get_definition_list(definition_text):
    """
    Retrieves a list of definitions delimited by \\enddesc
    """
    definition_list = definition_text.split('\\enddesc')
    for definition in definition_list[:-1]:
        yield definition.split('\\begindesc')[-1]


def compile_entries(section):
    """
    Iterates over each 'section' file and writes each
    definition within that file to its own file.
    Also returns a 'range' object to access the files.
    """
    src_text = Path('sections', section + '.tex').read_text()
    index_dir = Path('input', section, 'index')
    index_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Now indexing definitions for the '%s' section.", section)
    for entry_index, entry in enumerate(get_definition_list(src_text)):
        index_file = index_dir.joinpath( str(entry_index) + '.tex' )
        linelist = entry.split('\n')
        linelist.insert(0, '\\input macros')
        linelist.insert(1, '\\begindescriptions')
        linelist.insert(2, '\\begindesc')
        linelist.append('\\enddesc')
        linelist.append('\\enddescriptions')
        linelist.append('\\end')
        index_file.write_text( '\n'.join(linelist) )
    logger.info("Finished indexing definitions. Returning index iterator.")
    return range(len(definition_list))


def compile_cmd_list():
    """
    Reads the command index in 'book.sdx' and constructs
    a list of commands to be iterated over in Python.
    """
    linelist = Path('book.sdx').read_text().split('\n')
    cmd_list = set()
    logger.info("Now compiling command list from 'book.sdx'.")
    for line in linelist:
        cmd = re.search('^\\\\indexentry \{0\}\{(\w+)\}\{C\}.*$', line)
        if cmd is None:
            continue
        cmd_list.add(cmd.groups()[0])
    logger.info("Compilation complete. Returning command list.")
    return cmd_list


def write_cmd_definition(filename, command, section):
    """
    Checks if the given command is in the file
    specified, then copies the file per command
    and section specified.
    """
    index_text = filename.read_text()
    if re.search(f'\\\\cts\w* {command} .*', index_text) is None:
        return
    def_file = Path('input', section, command + '.tex')
    if def_file.exists():
        logger.warning("Error encountered with '%s' command in '%s' section. Skipping.", command, section)
        return
    def_file.write_text(index_text)


def main():
    """
    Iterates over command list, and typesets
    each command in accordance with its presence
    in each definition-file.
    """
    logger.info("Deleting 'input' directory.")
    rmtree('input', ignore_errors=True)
    SECTION_LIST = ('genops', 'math', 'modes', 'pages', 'paras')
    COMMAND_LIST = compile_cmd_list()
    for section in SECTION_LIST:
        entry_index_list = compile_entries(section)
        for command in COMMAND_LIST:
            for entry_index in entry_index_list:
                src_file = Path('input', section, 'index', str(entry_index) + '.tex')
                write_cmd_definition(src_file, command, section)

def compile_concept_list():
    """
    Reads 'kernel2/concepts.tex' to compile a list of concepts.
    """
    # test this function
    logger.info("Reading 'kernel2/concepts.tex' to compile list of concepts.")
    src_text = Path('kernel2', 'concepts.tex').read_text()
    concept_list = list()
    for line in src_text.split('\n'):
        concept = re.fullmatch("\\\\concept ?\{?([\\\\a-zA-Z ]+)\}?\s*", line)
        if concept is None:
            continue
        concept_list.append( concept.groups()[0].replace(' ', '-') )
    logger.info("Concept list compiled.")
    return concept_list

def main2():
    """
    Compiles a list of concepts in chapter four, 'Concepts'.
    Writes each concept to its own file in output/concepts/.
    """
    src_text = Path('kernel2', 'concepts.tex').read_text()
    # Make a function returning this.
    definition_text = src_text.split('\\beginconcepts')[-1].split('\\endconcepts')[0]
    # Make a function returning this.
    definition_list = [definition for definition in definition_text.split('\\endconcept')]
    definition_list.pop()
    concept_list = compile_concept_list()
    assert len(concept_list) == len(definition_list)
    index_dir = Path('output', 'concepts')
    logger.info("Now remaking '%s'.", str(index_dir))
    rmtree(str(index_dir), ignore_errors=True)
    index_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Now indexing concepts.")
    for entry_name, entry in zip(concept_list, definition_list):
        index_file = index_dir.joinpath( entry_name.strip('\\') + '.tex' )
        linelist = re.sub("\\\\pagebreak", "", entry).split('\n')
        linelist.insert(0, '\\input macros')
        linelist.insert(1, '\\beginconcepts')
        linelist.append('\\endconcept')
        linelist.append('\\endconcepts')
        linelist.append('\\end')
        index_file.write_text( '\n'.join(linelist) )

if __name__ == '__main__':
    from sys import argv
    try:
        logging.basicConfig(level=logging.INFO)
        {
                'definitions': main, # output definition dvi's
                'concepts': main2 # output the rest of `TeX for the Impatient'
                }[argv[1]]()
    except (IndexError, KeyError):
        print("Please choose one of either 'definitions' or 'concepts' as an argument.")
