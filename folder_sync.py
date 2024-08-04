import argparse
import os
import logging

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

#2 SETUP LOGGING

def setup_logging(log_file):
    logger = logging.getLogger('folder_sync')
    logger.setLevel(logging.DEBUG)

    # Check if log_file is a directory
    if os.path.isdir(log_file):
        log_file = os.path.join(log_file, 'sync.log')

    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Check if the log file is writable or can be created
    if os.path.exists(log_file):
        if not os.access(log_file, os.W_OK):
            raise PermissionError(f"Log file '{log_file}' is not writable.")
    else:
        # Check if the directory is writable
        if not os.access(log_dir, os.W_OK):
            raise PermissionError(f"Log directory '{log_dir}' is not writable.")

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file)

    # Set logging level for handlers
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)

    # Create formatters and add them to the handlers
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Example usage
args = parse_arguments()
args.source, args.replica, args.log_file = validate_paths(args.source, args.replica, args.log_file)
args.interval = validate_interval(args.interval)

logger = setup_logging(args.log_file)

logger.info(f"Source folder: {args.source}")
logger.info(f"Replica folder: {args.replica}")
logger.info(f"Logs folder: {args.log_file}")
logger.info(f"Sync interval: {args.interval} seconds")