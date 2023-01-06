# Angr auto reversing
## How to start
- main control script: `run_reverse.sh`
```
bash run_reverse.sh

# Run the script with
#   $ bash run_reverse.sh [-d <directory>] [-f <file>] [-l <file>]

#     -d    The directory with binaries to be reversed
#     -f    The file to be reversed
#     -l    The file with a list of files to be reversed
```
- config file: `reverse.conf`

| Var | Desc | Level |
| --- | ---  | ---   |
| LOG_DIR  | directory to save logs         | |
| CFG_DIR  | directory to save cfg files    | |
| MODE     | debugging level                | debug, info, warning, error, critical |
| WORKERS  | maximum number of processes    | |
| TIMEOUT  | timeout in seconds             | |
| FIN_LIST | list of finish paths           | |
| SKIP     | skip analyzed files            | 0: do not skip, 1: skip all|

- main script: `reverse_cfg.py`

## Example
### To start
```
# terminal 1
bash run_reverse.sh -d mybinaries/ > run.log
```
### To monitor
```
# terminal 2
tail -f run.log
```
### To terminate
```
# terminal 1
<CTRL + C>
## waiting for tasks that are still running to finish
```