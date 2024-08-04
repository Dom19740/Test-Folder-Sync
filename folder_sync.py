import argparse
import os
import time
from logging_setup import setup_logging
from file_operations import compare_files, copy_files_and_directories, remove_files_and_directories

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, help='Path to the log file or directory')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    return parser.parse_args()

def validate_paths(source, replica, log_file):
    """Validate the existence of the provided paths."""
    paths = [('source', source), ('replica', replica), ('log file', log_file)]
    while any(not os.path.exists(path) for name, path in paths):
        for i, (name, path) in enumerate(paths):
            if not os.path.exists(path):
                new_path = input(f"{name.capitalize()} path '{path}' does not exist. Please enter a valid {name} path: ")
                paths[i] = (name, new_path)
    return paths[0][1], paths[1][1], paths[2][1]

def validate_interval(interval):
    while True:
        try:
            interval = int(interval)
            if interval <= 0:
                raise ValueError
            return interval
        except ValueError:
            interval = input("Invalid interval. Please enter a valid synchronization interval in seconds: ")

def sync_folders(source, replica, logger):
    """Synchronize the source folder with the replica folder."""
    try:
        source_items = os.listdir(source)
        replica_items = os.listdir(replica)

        for item in source_items:
            source_item_path = os.path.join(source, item)
            replica_item_path = os.path.join(replica, item)

            if os.path.isdir(source_item_path):
                if item not in replica_items:
                    logger.info(f"Copying directory {source_item_path} to {replica_item_path}")
                    copy_files_and_directories(source_item_path, replica_item_path)
                else:
                    sync_folders(source_item_path, replica_item_path, logger)
            else:
                if item not in replica_items or not compare_files(source_item_path, replica_item_path, method='md5'):
                    logger.info(f"Copying file {source_item_path} to {replica_item_path}")
                    copy_files_and_directories(source_item_path, replica_item_path)

        for item in replica_items:
            if item not in source_items:
                replica_item_path = os.path.join(replica, item)
                logger.info(f"Removing {replica_item_path}")
                remove_files_and_directories(replica_item_path)

    except PermissionError as e:
        logger.error(f"Permission error: {e}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"Error during synchronization: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    args.source, args.replica, args.log_file = validate_paths(args.source, args.replica, args.log_file)
    args.interval = validate_interval(args.interval)
    
    logger = setup_logging(args.log_file)
    
    logger.info(f"Source folder: {args.source}")
    logger.info(f"Replica folder: {args.replica}")
    logger.info(f"Logs folder: {args.log_file}")
    logger.info(f"Sync interval: {args.interval} seconds")

    while True:
        sync_folders(args.source, args.replica, logger)
        time.sleep(args.interval)