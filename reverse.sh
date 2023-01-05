#!/bin/bash

source reverse.conf
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
START $fpath
timeout --kill-after=5s "$TIMEOUT"s python reverse_cfg.py -f $fpath -m $MODE -o $CFG_DIR 2> "logs/$(basename $fpath)"
FINISH $fpath