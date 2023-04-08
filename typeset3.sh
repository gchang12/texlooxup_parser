#!/bin/bash
output_dir="output/concepts";
for kernel in {config,eplain,macros,fonts}; do (
    cp kernel/$kernel.tex $output_dir;
); done;
cd $output_dir;
for texfile in *.tex; do (
    case "$texfile" in
        "config.tex") false
            ;;
        "eplain.tex") false
            ;;
        "macros.tex") false
            ;;
        "fonts.tex") false
            ;;
        *) pdftex -output-format dvi -interaction batchmode $texfile;
    esac;
); done;
rm *.aux *.idx *.log *.tex *.ccs;
