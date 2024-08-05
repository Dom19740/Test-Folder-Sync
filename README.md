# Test-Folder-Sync

## Test Task

### Task Description

Implement a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of the source folder in the replica folder.

### Accepted Programming Languages

- Python
- C#

### Requirements

1. Synchronization must be one-way: after synchronization, the content of the replica folder should be modified to exactly match the content of the source folder.
2. Synchronization should be performed periodically.
3. File creation/copying/removal operations should be logged to a file and to the console output.
4. Folder paths, synchronization interval, and log file path should be provided using command line arguments.
5. It is undesirable to use third-party libraries that implement folder synchronization.
6. It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library;

### Submission

The solution should be presented as a link to a public GitHub repository.

### Additional Notes

- Avoid implementing common algorithms (like MD5 calculation) from scratch. Use built-in or well-established third-party libraries for such functionalities.
- Focus on implementing the core synchronization logic and command-line interface.
- Ensure proper error handling and logging throughout the program.

## Usage

To run the Folder Synchronization Script, use the following command:

```sh
python main.py -s <source_directory> -r <replica_directory> -l <log_directory> -i <interval_in_seconds>

## Example

python main.py -s C:\source -r C:\replica -l C:\logs -i 10

## Arguments
-s, --source: Path to the source directory.
-r, --replica: Path to the replica directory.
-l, --log_file: Path to the log directory.
-i, --interval: Synchronization interval in seconds.