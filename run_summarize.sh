#!/bin/bash

source summarize.conf

usage() {
    echo "Run the script with"
    echo "  $ bash $0 [-d <directory>] [-f <file>] [-l <file>]"
    echo
    echo "    -d    The directory to CFG pickle files"
    echo "    -f    The file to be summarized"
    echo "    -l    The file with a list of files to be summarized"
}

sum_run() {
    fname=$(basename $1)
    echo "[RUN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

sum_fin() {
    fname=$(basename $1)
    echo "[FIN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

summarize() {
    source summarize.conf

    [[ $1 == '' ]] && echo 'File path not provided' && exit 1
    fpath=$1

    sum_run $fpath
    
    # main section
    python $MAIN_SCRIPT --method $METHOD -f $fpath -s $SAVE_DIR

    sum_fin $fpath
}


[[ $1 == '' ]] && usage && exit 0
mkdir -p $SAVE_DIR

input=$1
export -f summarize
export -f sum_run
export -f sum_fin

while getopts "ho:d:f:l:" argv; do
    case $argv in
        h )
            usage
            exit 0
            ;;
            
        d )
            dir=$OPTARG
            [[ -d $dir ]] || (echo 'Invalid Directory' && usage && exit 1)
            find $dir -type f -name '*.pickle' | xargs -P $WORKERS -I {} bash -c "summarize {}"
            ;;

        f )
            file=$OPTARG
            [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
            bash -c "summarize $file"
            ;;

        l )
            list=$OPTARG
            [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)
            cat $list | xargs -P $WORKERS -I {} bash -c "summarize {}"
            ;;

        ? )
            usage
            exit 1
            ;;
    esac
done
