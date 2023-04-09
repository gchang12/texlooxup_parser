#!/bin/bash
echo "Remaking 'output' directory.";
rm -r output;
mkdir -p output;
cd output;
for i in {genops,math,modes,pages,paras}; do (
    mkdir $i;
    cp ../kernel/*.tex ./$i/;
    cp ../input/$i/*.tex ./$i/;
    cd $i;
    (for j in *.tex; do (
        case "$j" in
            "config.tex") false
                ;;
            "eplain.tex") false
                ;;
            "macros.tex") false
                ;;
            "fonts.tex") false
                ;;
            *) (echo -n "Now processing '$i/$j'... "; pdftex -output-format dvi -interaction batchmode $j 1>/dev/null && echo "OK" || echo "Failed";);
                ;;
        esac); done);
    rm *.tex *.aux *.idx *.log;
    echo "tex, aux, idx, log files removed from 'output/$i' folder.";
    cd ..;
); done;
echo "genops, math, modes, pages, and paras folders saved in 'output'.";
