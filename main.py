"""
Gets a list of TeX commands from `book.sdx'
"""

import re
from pathlib import Path
from shutil import rmtree

SECTION_LIST = ("genops", "paras", "math", "modes", "pages")

def get_command_list():
    """
    Returns a list of TeX commands listed in
    `book.sdx', an index file of sorts.
    """
    # Each command is in a line of the form:
    # - "\indexentry {0}{...}{C}.*"
    pattern = "\\\\indexentry \{0\}\{(.+)\}\{C\}.*"
    command_list = []
    linelist = Path('book.sdx').read_text().split('\n')
    for line in linelist:
        match = re.fullmatch(pattern, line)
        if not match:
            continue
        command_list.append(match.groups()[0])
    return command_list


def get_command_definitions(tex_command):
    """
    Returns a dict of indices, each corresponding to
    a definition tied to the TeX command passed as a parameter.
    """
    if tex_command[0] == '\\':
        return {}
    entry_dict = {}
    root = "sections/"
    error_lines = {}
    for section in SECTION_LIST:
        entry_index = 0
        entry_dict[section] = set()
        linelist = Path(root, section + ".tex").read_text().split('\n')
        for line in linelist:
            if line == '\\begindescr':
                entry_index += 1
                continue
            try:
                if re.search(f"\\\\cts\w* {tex_command} ", line) is None:
                    continue
            except re.error:
                try:
                    error_lines[section].append(line)
                except KeyError:
                    error_lines[section] = []
            if entry_index:
                entry_dict[section].add(entry_index)
        if not entry_dict[section]:
            entry_dict.pop(section)
    with open('error_lines.log', 'a') as wfile:
        for section, linelist in entry_dict.items():
            for line in linelist:
                error_line = f"{section}: {line}"
                print(error_line, file=wfile)
    return entry_dict


def generate_entries(section):
    """
    Writes each TeX definition to file by index.
    Each file will be saved in accordance with the following structure.
    - ./input/{section}/{entry_index}.tex
    """
    write_mode = False
    entry_index = 0
    entry_dict = {}
    # Compile sections into dict
    linelist = Path('sections', section + '.tex').read_text().split('\n')
    for line in linelist:
        if re.search("\\\\(begin|end)desc[^r]?", line) is not None:
            write_mode = not write_mode
            entry_index += write_mode
        if write_mode and re.search('\\\\(sub)?section', line) is None:
            try:
                entry_dict[entry_index].append(line)
            except KeyError:
                entry_dict[entry_index] = [line]
    print(entry_dict)
    raise Exception
    # Write sections to file by index
    input_path = Path('input', section, 'index')
    input_path.mkdir(parents=True, exist_ok=True)
    for entry_index, linelist in entry_dict.items():
        linelist.insert(0, "\\input macros")
        linelist.insert(1, "\\begindescriptions")
        linelist.append("\\enddescriptions")
        entry_path = input_path.joinpath( str(entry_index) + '.tex' )
        entry_path.write_text( '\n'.join(linelist) )


def main():
    """
    Generate index.
    Generate entries from index.
    Write each entry to pdf.
    """
    rmtree('input', ignore_errors=True)
    for section in SECTION_LIST:
        generate_entries(section)
    for tex_command in get_command_list():
        entry_dict = get_command_definitions(tex_command)
        for section, index_list in entry_dict.items():
            root_path = Path('input', section)
            for entry_index in index_list:
                src_path = root_path.joinpath('index', str(entry_index) + '.tex')
                tgt_path = root_path.joinpath(tex_command + '.tex')
                iteration = 1
                while tgt_path.exists():
                    tgt_path = root_path.joinpath(
                            tex_command + str(iteration) + '.tex'
                            )
                    iteration += 1
                print(section, entry_index, tex_command)
                tgt_path.write_text( src_path.read_text() )


if __name__ == '__main__':
    main()
