<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/texdict_generator.svg?branch=main)](https://cirrus-ci.com/github/<USER>/texdict_generator)
[![ReadTheDocs](https://readthedocs.org/projects/texdict_generator/badge/?version=latest)](https://texdict_generator.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/texdict_generator/main.svg)](https://coveralls.io/r/<USER>/texdict_generator)
[![PyPI-Server](https://img.shields.io/pypi/v/texdict_generator.svg)](https://pypi.org/project/texdict_generator/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/texdict_generator.svg)](https://anaconda.org/conda-forge/texdict_generator)
[![Monthly Downloads](https://pepy.tech/badge/texdict_generator/month)](https://pepy.tech/project/texdict_generator)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/texdict_generator)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# texdict_generator

> Add a short description here!

A longer description of your project goes here...

ABOUT
===
This program creates a compendium of Plain TeX commands, as listed in _TeX for the Impatient_, by Paul Abrahams, Karl Berry, and Kathryn Hargreaves. You can find a link to the book, which has been made open-source, [here](https://ctan.org/pkg/impatient).

After building the program, looking up Plain TeX commands is as simple as changing to the root of this project directory, invoking python on query.py, specifying arguments as desired, and selecting the index number corresponding to the command you wish to query.

You can search by pattern, by section, or by both.

HOW TO BUILD
===
`make clean`  
`make`

HOW TO USE
===
`python query.py {pattern} [-section [section, ...]]`

EXAMPLES
===
Searching for the pattern '`par`' in sections `[genops, paras]`  
`python query.py par -section genops para`

    pattern: 'par'
    sections: genops, math
    
    5 results found\.
    =============================
      0: math/parallel
      1: math/uparrow
      2: math/Uparrow
      3: math/partial
      4: genops/tracingparagraphs

Searching for the pattern '`par`' in all sections.  
`python query.py par`

    pattern: 'par'
    sections: concepts, genops, math, miscellany, modes, pages, paras
    
    13 results found.
    =============================
      0: math/parallel
      1: math/uparrow
      2: math/Uparrow
      3: math/partial
      4: pages/parskip
      5: concepts/paragraph
      6: concepts/parameter
      7: genops/tracingparagraphs
      8: paras/parfillskip
      9: paras/everypar
     10: paras/parshape
     11: paras/parindent
     12: paras/par

Searching for commands in the section '`paras`'.  
`python query.py -section paras`

    pattern: '.*'
    sections: paras
    
    142 results found.
    ===============================
      0: paras/_italiccorrection
      1: paras/S
      2: paras/P
      3: paras/obeyspaces
      4: paras/AE
      ...


<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
