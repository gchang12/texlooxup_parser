cd ./output/;
# Check if argument is null, then decide.
if [ -z "$1" ]; then
    echo -e "\n    Please pass either a control word or section as an argument. e.g.\n";
    echo "    'texdict par', 'texdict input', etc.";
    echo -e "    'texdict -{section}', where section is one of:\n$(ls | sed s/^/"        "/g)";
else
    # Determine whether or not to search by section.
    if [ "${1::1}" == "-" ]; then
        fname_list=($(ls */*.dvi | grep -P ".*${1#-}.*(?=/)"));
    else
        fname_list=($(ls */*.dvi | grep -P "$1(?=[^/]*\.dvi)"));
    fi;
    # Check if selection list is empty, then decide.
    if [ -z "$fname_list" ]; then
        printf "\"$1\" not found.";
    else
        dvi_reader="okular";
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
fi;
echo;
cd ..;
