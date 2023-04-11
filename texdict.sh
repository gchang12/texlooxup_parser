dvi_reader="okular";
cd ./output/;

# Determine whether or not to search by section.
if [ "${1::1}" == "-" ]; then
    fname_list=($(ls */*.dvi | grep -P ".*${1#-}.*(?=/)"));
else
    fname_list=($(ls */*.dvi | grep -P "$1(?=[^/]*\.dvi)"));
fi;

# Execute action based on parameter and resultset
if [ -z "$1" ]; then
    echo -e "Please pass either a control word or section as an argument.\n";
    echo "e.g. 'texdict par'  or 'texdict input'";
    echo -e "'texdict -{section}', where section is one of:\nconcepts, genops, math, modes, paras, pages, miscellany";
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
        $dvi_reader $fname 2>/dev/null;
    fi;
fi;
echo;
cd ..;
