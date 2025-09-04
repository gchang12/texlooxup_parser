
from pathlib import Path
import json

filelist = []
target_file = "../../app/excerptList.ts"

for excerptdir in filter(lambda p: p.is_dir(), Path('.').iterdir()):
    for excerptfile in excerptdir.iterdir():
        filelist.append((str(excerptdir), excerptfile.name))

with open(target_file, encoding="utf-8", mode="w") as wfile:
    json.dump(filelist, wfile, indent=2)
