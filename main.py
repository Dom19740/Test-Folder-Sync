import argparse
import os
import time
from logging_setup import setup_logging
from file_operations import compare_files, copy_files_and_directories, remove_files_and_directories

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument('-s', '--source', dest="source", type=str, required=True, help='Path to the source folder')
    parser.add_argument('-r', '--replica', dest="replica", type=str, required=True, help='Path to the replica folder')
    parser.add_argument('-l', '--log', dest="log", type=str, required=True, help='Path to the log folder')
    parser.add_argument('-i', '--interval', dest="interval", type=int, required=True, help='Synchronization interval in seconds')
    return parser.parse_args()

# Example usage:
# python main.py -s C:\source -r C:\replica -l C:\logs -i 120

def validate_paths(source, replica, log):
    """Validate the existence of the provided paths."""
    paths = [('source', source), ('replica', replica), ('log file', log)]
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
    changes_made = 0
    try:
        source_items = os.listdir(source)
        replica_items = os.listdir(replica)

        for item in source_items:
            source_item_path = os.path.join(source, item)
            replica_item_path = os.path.join(replica, item)

            if os.path.isdir(source_item_path):
                if item not in replica_items:
                    logger.info(f"Copying folder {source_item_path} to {replica_item_path}")
                    copy_files_and_directories(source_item_path, replica_item_path)
                    changes_made += 1
                else:
                    changes_made += sync_folders(source_item_path, replica_item_path, logger)
            else:
                if item not in replica_items or not compare_files(source_item_path, replica_item_path, method='md5'):
                    logger.info(f"Copying file {source_item_path} to {replica_item_path}")
                    copy_files_and_directories(source_item_path, replica_item_path)
                    changes_made += 1

        for item in replica_items:
            if item not in source_items:
                replica_item_path = os.path.join(replica, item)
                logger.info(f"Removing {replica_item_path}")
                remove_files_and_directories(replica_item_path)
                changes_made += 1

        return changes_made

    except PermissionError as e:
        logger.error(f"Permission error: {e}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"Error during synchronization: {e}")
    return 0

if __name__ == "__main__":
    args = parse_arguments()
    args.source, args.replica, args.log = validate_paths(args.source, args.replica, args.log)
    args.interval = validate_interval(args.interval)

    logger = setup_logging(args.log)
    
    logger.info(f"Source folder: {args.source}")
    logger.info(f"Replica folder: {args.replica}")
    logger.info(f"Logs folder: {args.log}")
    logger.info(f"Sync interval: {args.interval} seconds")

    while True:
        changes_made = sync_folders(args.source, args.replica, logger)
        if changes_made > 0:
            logger.info(f"Synchronization completed successfully. {changes_made} changes made.")
        else:
            logger.info("No files changed.")
        time.sleep(args.interval)