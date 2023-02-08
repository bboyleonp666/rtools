#!/bin/bash

source summarize.conf

[[ $1 == '' ]] && echo 'File path not provided' && exit 1
fpath=$1

START() {
    fname=$(basename $1)
    echo "[RUN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

FINISH() {
    fname=$(basename $1)
    echo "[FIN] [$(date '+%Y%m%d-%H%M%S.%N')] | FILE: $fname"
}

# main section
START $fpath
python $MAIN_SCRIPT --method $METHOD -f $fpath -s $SAVE_DIR
FINISH $fpath