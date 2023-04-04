#!/bin/bash
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
            *) pdftex -output-format dvi -interaction batchmode $j;
                ;;
        esac); done);
    rm *.tex *.aux *.idx *.log;
    cd ..
); done
