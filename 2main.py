import re
from pathlib import Path

filename = 'sections/genops.tex'

file_ = Path(filename).read_text()
print(file_[:100])
entries = re.search("\\\\begindesc(.+)\\\\enddesc", file_)
print(entries.groups())
