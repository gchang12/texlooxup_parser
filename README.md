ABOUT
===
This program creates a compendium of Plain TeX commands, as listed in _TeX for the Impatient_, by Paul Abrahams, Karl Berry, and Kathryn Hargreaves. You can find a link to the book, which has been made open-source, [here](https://ctan.org/pkg/impatient).

After building the program, looking up Plain TeX commands is as simple as changing to the root of this project directory, invoking python on query.py, and specifying arguments as desired.

You can search by pattern, by section, or by both.

HOW TO BUILD
===
---
`make clean`
`make`

HOW TO USE
===
---
`python query.py {pattern} [-section [section, ...]]`
