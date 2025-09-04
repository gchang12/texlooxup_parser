from pathlib import Path
import json

filelist = []

for excerptdir in filter(lambda p: p.is_dir(), Path('.').iterdir()):
    for excerptfile in excerptdir.iterdir():
        filelist.append((str(excerptdir), excerptfile.name))

sorted_filelist = sorted(filelist, key=lambda dir_file: dir_file[1].lower().lstrip('_'))

with open("../../app/excerptList.ts", encoding="utf-8", mode="w") as wfile:
    json.dump(sorted_filelist, wfile, indent=2)

