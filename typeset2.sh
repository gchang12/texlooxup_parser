#!/bin/bash
miscellany_dir="output/miscellany";
rm -r $miscellany_dir;
mkdir -p $miscellany_dir;
for kernel in {config,eplain,macros,fonts}; do (
    cp kernel/$kernel.tex $miscellany_dir;
); done;
for section in {usebook,usingtex,examples,tips,errors,usermacs,capsule}; do (
    cp kernel2/$section.tex $miscellany_dir;
    cd $miscellany_dir;
    pdftex -output-format dvi -interaction batchmode $section;
    cd ../../;
) done;
cd $miscellany_dir;
rm *.aux *.idx *.log *.tex;
