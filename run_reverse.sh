#!/bin/bash

source reverse.conf
input=$1

usage() {
    echo "Run the script with"
    echo "  $ bash $0 [-d <directory>] [-f <file>] [-l <file>]"
    echo
    echo "    -d    The directory with binaries to be reversed"
    echo "    -f    The file to be reversed"
    echo "    -l    The file with a list of files to be reversed"
}

[[ $input == '' ]] && usage && exit 0

[[ $SKIP -eq 0 ]] && [[ -f $FIN_LIST ]] && rm $FIN_LIST && touch $FIN_LIST
[[ $(pip list | grep angr > /dev/null)$? -eq 1 ]] && echo "No module named 'angr'" && exit 1
while getopts "hd:f:l:" argv; do
    case $argv in
        h )
            usage
            exit 0
            ;;
        
        d )
            dir=$OPTARG
            [[ -d $dir ]] || (echo 'Invalid Directory' && usage && exit 1)

            if [[ $SHUFFLE -eq 1 ]]; then
                comm -3 <(find $dir -type f | sort) <(sort $FIN_LIST) | shuf | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            else
                comm -3 <(find $dir -type f | sort) <(sort $FIN_LIST) | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            fi
            ;;

        f )
            file=$OPTARG
            [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
            bash $RUN_SCRIPT $file
            ;;

        l )
            list=$OPTARG
            [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)

            if [[ $SHUFFLE -eq 1 ]]; then
                comm -3 <(sort $list) <(sort $FIN_LIST) | shuf | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            else
                comm -3 <(sort $list) <(sort $FIN_LIST) | xargs -P $WORKERS -n 1 bash $RUN_SCRIPT
            fi
            ;;

        ? )
            usage
            exit 1
            ;;
    esac
done
