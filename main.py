"""
"""

import re
from pathlib import Path
from shutil import rmtree

def compile_entries(section):
    """
    """
    src_text = Path('sections', section + '.tex').read_text()
    definition_text = src_text.split('\\begindescriptions')[-1].split('\\enddescriptions')[0]
    definition_list = [definition.split('\\begindesc')[-1] for definition in definition_text.split('\\enddesc')]
    definition_list.pop()
    index_dir = Path('input', section, 'index')
    index_dir.mkdir(parents=True, exist_ok=True)
    for entry_index, entry in enumerate(definition_list):
        index_file = index_dir.joinpath( str(entry_index) + '.tex' )
        linelist = entry.split('\n')
        linelist.insert(0, '\\input macros')
        linelist.insert(1, '\\begindescriptions')
        linelist.insert(2, '\\begindesc')
        linelist.append('\\enddesc')
        linelist.append('\\enddescriptions')
        linelist.append('\\end')
        index_file.write_text( '\n'.join(linelist) )
    return range(len(definition_list))


def compile_cmd_list():
    """
    book.sdx
    """
    linelist = Path('book.sdx').read_text().split('\n')
    cmd_list = set()
    for line in linelist:
        cmd = re.search('^\\\\indexentry \{0\}\{(\w+)\}\{C\}.*$', line)
        if cmd is None:
            continue
        cmd_list.add(cmd.groups()[0])
    return cmd_list


def write_cmd_definition(filename, command, section):
    """
    """
    index_text = filename.read_text()
    if re.search(f'\\\\cts\w* {command} .*', index_text) is None:
        return
    def_file = Path('input', section, command + '.tex')
    if def_file.exists():
        print(filename, command, section)
        raise Exception
    def_file.write_text(index_text)


def main():
    """
    """
    rmtree('input', ignore_errors=True)
    SECTION_LIST = ('genops', 'math', 'modes', 'pages', 'paras')
    COMMAND_LIST = compile_cmd_list()
    for section in SECTION_LIST:
        entry_index_list = compile_entries(section)
        for command in COMMAND_LIST:
            #print(command)
            for entry_index in entry_index_list:
                src_file = Path('input', section, 'index', str(entry_index) + '.tex')
                write_cmd_definition(src_file, command, section)

if __name__ == '__main__':
    main()
