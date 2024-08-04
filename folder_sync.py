import argparse
import os
from logging_setup import setup_logging  # Import the logging setup

# 1. PARSE COMMAND LINE ARGUMENTS

def parse_arguments():
    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, help='Path to the log file or directory')
    parser.add_argument('interval', type=str, help='Synchronization interval in seconds')
    return parser.parse_args()

# Invalid path error handling
def validate_paths(source, replica, log_file):
    paths = [('source', source), ('replica', replica), ('log file', log_file)]
    while any(not os.path.exists(path) for name, path in paths):
        for i, (name, path) in enumerate(paths):
            if not os.path.exists(path):
                paths[i] = (name, input(f"{name.capitalize()} path '{path}' does not exist. Please enter a valid {name} path: "))
    return paths[0][1], paths[1][1], paths[2][1]

# Invalid interval error handling
def validate_interval(interval):
    while True:
        try:
            interval = int(interval)
            if interval <= 0:
                raise ValueError
            return interval
        except ValueError:
            interval = input("Invalid interval. Please enter a valid synchronization interval in seconds: ")

# Example usage
args = parse_arguments()
args.source, args.replica, args.log_file = validate_paths(args.source, args.replica, args.log_file)
args.interval = validate_interval(args.interval)

logger = setup_logging(args.log_file)

logger.info(f"Source folder: {args.source}")
logger.info(f"Replica folder: {args.replica}")
logger.info(f"Logs folder: {args.log_file}")
logger.info(f"Sync interval: {args.interval} seconds")