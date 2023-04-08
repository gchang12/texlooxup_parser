#!/bin/bash
miscellany_dir="output/miscellany";
echo "Remaking '$miscellany_dir'.";
rm -r $miscellany_dir;
mkdir -p $miscellany_dir;
for kernel in {config,eplain,macros,fonts}; do (
    cp kernel/$kernel.tex $miscellany_dir;
); done;
for section in {usebook,usingtex,examples,tips,errors,usermacs,capsule}; do (
    cp kernel2/$section.tex $miscellany_dir;
    cd $miscellany_dir;
    (echo "Now processing $section.tex"; pdftex -output-format dvi -interaction batchmode $section 1>/dev/null && echo "'$section.tex' processed successfully.");
    cd ../../;
); done;
cd $miscellany_dir;
rm *.aux *.idx *.log *.tex;
echo "aux, idx, log, tex, ccs files removed.";
