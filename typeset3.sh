#!/bin/bash
output_dir="output/concepts";
echo "Preparing '$output_dir' folder for typeset operations.";
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
        *) (echo -n "Now processing '$texfile'... "; pdftex -output-format dvi -interaction batchmode $texfile 1>/dev/null && echo "OK" || echo "Failed";);
    esac;
); done;
rm *.aux *.idx *.log *.tex *.ccs;
echo "aux, idx, log, tex, ccs files removed.";
echo "'concepts' folder saved in 'output'.";
