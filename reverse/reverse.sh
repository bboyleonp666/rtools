#!/bin/bash

source reverse.conf

[[ $1 == '' ]] && echo 'File Path not provided' && exit 1
fpath=$1

START() {
    fname=$(basename $1)
    echo "[RUN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

FINISH() {
    fname=$(basename $1)
    echo "[FIN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

mkdir -p $LOG_DIR
touch $FIN_LIST

# main section
START $fpath
timeout --kill-after=5s "$TIMEOUT"s \
    python $MAIN_SCRIPT -f $fpath -m $MODE -o $CFG_DIR 2> "logs/$(basename $fpath).log" \
    && echo $fpath >> $FIN_LIST
FINISH $fpath