#!/bin/bash

source summarize.conf
input=$1

usage() {
    echo "Run the script with"
    echo "  $ bash $0 [-d <directory>] [-f <file>] [-l <file>]"
    echo
    echo "    -d    The directory to CFG pickle files"
    echo "    -f    The file to be summarized"
    echo "    -l    The file with a list of files to be summarized"
}


[[ $input == '' ]] && usage && exit 0
mkdir -p $SAVE_DIR
while getopts "ho:d:f:l:" argv; do
    case $argv in
        h )
            usage
            exit 0
            ;;
            
        d )
            dir=$OPTARG
            [[ -d $dir ]] || (echo 'Invalid Directory' && usage && exit 1)
            find $dir -type f -name *.pickle | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            ;;

        f )
            file=$OPTARG
            [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
            bash $RUN_SCRIPT $file
            ;;

        l )
            list=$OPTARG
            [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)
            cat $list | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            ;;

        ? )
            usage
            exit 1
            ;;
    esac
done