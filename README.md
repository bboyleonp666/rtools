# Angr auto reversing
## Reverse
- main control script: `run_reverse.sh`
- usage
    ```
    $ bash run_reverse.sh

    # Run the script with
    #   $ bash run_reverse.sh [-d <directory>] [-f <file>] [-l <file>]

    #     -d    The directory with binaries to be reversed
    #     -f    The file to be reversed
    #     -l    The file with a list of files to be reversed
    ```

- config file: `reverse.conf`

    | Var         | Desc | Option |
    | ---         | ---  | ---    |
    | MAIN_SCRIPT | location to the main reversing script |                                   |
    | RUN_SCRIPT  | location to the run script            |                                   |
    | LOG_DIR     | directory to save logs                |                                   |
    | CFG_DIR     | directory to save cfg files           |                                   |
    | MODE        | debugging level                | debug, info, warning, error, critical    |
    | WORKERS     | maximum number of processes    |                                          |
    | TIMEOUT     | timeout in seconds             |                                          |
    | FIN_LIST    | list of finish paths           |                                          |
    | SKIP        | skip analyzed files            | 0) do not skip<br>1) skip all            |
    | SHUFFLE     | analyze in random order        | 0) in sorted order<br>1) in random order |

- example
    1. start run
        ```
        # terminal 1
        bash run_reverse.sh -d mybinaries/ > /tmp/run.log
        ```
    2. monitor progress
        ```
        # terminal 2
        tail -f run.log
        ```
    3. terminate
        ```
        # terminal 1
        <CTRL + C>  # and wait for the running processes to finish
        ```

## Summarize
- main control script: `run_summarize.sh`
- usage
    ```
    $ bash run_summarize.sh
    # Run the script with
    # $ bash run_summarize.sh [-d <directory>] [-f <file>] [-l <file>]

    #     -d    The directory to CFG pickle files
    #     -f    The file to be summarized
    #     -l    The file with a list of files to be summarized
    ```

- config file: `summarize.conf`

    | Var         | Desc | Option |
    | ---         | ---  | ---    |
    | MAIN_SCRIPT | location to the main summarizing script                | |
    | RUN_SCRIPT  | location to the run script which calls the main script | |
    | METHOD      | summarizing method to be proceeded                     | summary, opcode_blocks |
    | SAVE_DIR    | directory to save the extracted summary                | |
    | WORKERS     | maximum number of processes                            | |

- example
    1. start run
        ```
        bash run_summarize.sh -d CFGs/
        ```
    2. terminate
        ```
        <CTRL + C>  # and wait for the running processes to finish
        ```