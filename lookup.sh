pdf_reader="xr";
cd ./output/;
fname_list=($(ls */*.dvi | grep -P "$1(?=[^/]*\.dvi)"));
if [ -z "$fname_list" -o -z "$1" ]; then
    printf "\"$1\" not found.";
else
    echo;
    echo "    View a definition";
    echo "    =================";
    for ((i=0; i<${#fname_list[@]}; i=i+1)); do
        fname=${fname_list[$i]};
        printf "    %2d: %s\n" $i ${fname%.dvi};
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
