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

| Var | Desc |
| --- | ---  |
| LOG_DIR | directory to save logs      |
| CFG_DIR | directory to save cfg files |
| MODE    | debugging level             |
| WORKERS | maximum number of processes |
| TIMEOUT | timeout in seconds          |

- main script: `reverse_cfg.py`