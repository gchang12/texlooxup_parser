pdf_reader="okular";
cd ./output/;
if [ "$1" == "miscellany" -o "$1" == "misc" ]; then
    fname_list=($(ls miscellany/*.dvi));
else
    fname_list=($(ls */*.dvi | grep -P "$1(?=[^/]*\.dvi)"));
fi;
if [ -z "$1" ]; then
    printf "Pass either a control word or 'misc' as an argument.";
elif [ -z "$fname_list" ]; then
    printf "\"$1\" not found.";
else
    spacing=0;
    space_factor=1;
    while [[ "$space_factor" -lt ${#fname_list[@]} ]]; do
        space_factor=$((space_factor*10)); spacing=$((spacing+1));
    done;
    echo;
    echo "    View a definition";
    echo "    =================";
    for ((i=0; i<${#fname_list[@]}; i=i+1)); do
        fname=${fname_list[$i]};
        printf "    %*d: %s\n" $spacing $i ${fname%.dvi};
    done;
    echo;
    read -p ">   Please make a selection: ";
    fname=${fname_list[$REPLY]};
    if [[ "$REPLY" =~ ^[0-9]+$ && -n "$fname" ]]; then
        $pdf_reader $fname 2>/dev/null;
    fi;
fi;
echo;
cd ..;
