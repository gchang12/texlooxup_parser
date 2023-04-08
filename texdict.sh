pdf_reader="okular";
cd ./output/;
if [ "$1" = "miscellany" ]; then
    fname_list=($(ls miscellany/*.dvi));
else
    fname_list=($(ls */*.dvi | grep -P "$1(?=[^/]*\.dvi)"));
fi;
spacing=0;
space_factor=1;
if [ -z "$fname_list" -o -z "$1" ]; then
    printf "\"$1\" not found.";
else
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
        $pdf_reader $fname;
    fi;
fi;
echo;
cd ..;
