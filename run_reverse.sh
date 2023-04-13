#!/bin/bash

source reverse.conf

usage() {
    echo "Run the script with"
    echo "  $ bash $0 [-d <directory>] [-f <file>] [-l <file>]"
    echo
    echo "    -d    The directory with binaries to be reversed"
    echo "    -f    The file to be reversed"
    echo "    -l    The file with a list of files to be reversed"
}

rev_run() {
    fname=$(basename $1)
    echo "[RUN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

rev_fin() {
    fname=$(basename $1)
    echo "[FIN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

reverse() {
    source reverse.conf
    [[ $1 == '' ]] && echo 'File Path not provided' && exit 1
    fpath=$1

    rev_run $fpath

    # main section
    timeout --kill-after=5s "$TIMEOUT"s \
        python $MAIN_SCRIPT -f $fpath -m $MODE -o $CFG_DIR 2> "$LOG_DIR/$(basename $fpath).log"
    echo "$fpath,$?" >> $STATE_LIST  # $? records the state after reversing (fail or success)

    rev_fin $fpath
}


[[ $1 == '' ]] && usage && exit 0
mkdir -p $CFG_DIR
mkdir -p $LOG_DIR

[[ $SKIP -eq 0 ]] && [[ -f $STATE_LIST ]] && rm $STATE_LIST
touch $STATE_LIST
[[ $(pip list | grep angr > /dev/null)$? -eq 1 ]] && echo "No module named 'angr'" && exit 1

input=$1
export -f reverse
export -f rev_run
export -f rev_fin

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
                comm -3 <(find $dir -type f | sort) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | shuf | \
                    xargs -P $WORKERS -I {} bash -c "reverse {}"
            else
                comm -3 <(find $dir -type f | sort) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | \
                    xargs -P $WORKERS -I {} bash -c "reverse {}"
            fi
            ;;

        f )
            file=$OPTARG
            [[ -f $file ]] || (echo 'Invalid File' && usage && exit 1)
            bash -c "reverse $file"
            ;;

        l )
            list=$OPTARG
            [[ -f $list ]] || (echo 'Invalid File' && usage && exit 1)

            if [[ $SHUFFLE -eq 1 ]]; then
                comm -3 <(sort $list) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | shuf | \
                    xargs -P $WORKERS -I {} bash -c "reverse {}"
            else
                comm -3 <(sort $list) <(cat $STATE_LIST | cut -d ',' -f 1 | sort) | \
                    xargs -P $WORKERS -I {} bash -c "reverse {}"
            fi
            ;;

        ? )
            usage
            exit 1
            ;;
    esac
done
