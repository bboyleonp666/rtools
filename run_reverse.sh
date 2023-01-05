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

[[ $1 == '' ]] && usage && exit 0
while getopts "hd:f:l:" argv; do
    case $argv in
        h )
            usage
            exit 0
            ;;

        d )
            dir=$OPTARG
            [[ -d $dir ]] || (echo 'Invalid Directory' && usage && exit 1)
            find $dir -type f | xargs -P $WORKERS -n 1 bash reverse.sh
            ;;
            
        f )
            file=$OPTARG
            [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
            bash reverse.sh $file
            ;;

        l )
            list=$OPTARG
            [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)
            cat $list | xargs -P $WORKERS -n 1 bash reverse.sh
            ;;

        ? )
            usage
            exit 1
            ;;
    esac
done