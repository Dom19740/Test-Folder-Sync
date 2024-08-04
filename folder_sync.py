import argparse
import os

def get_valid_path(prompt, is_file=False):
    while True:
        path = input(prompt)
        if is_file:
            dir_path = os.path.dirname(path)
            if os.path.exists(dir_path):
                return path
            print(f"The directory for the log file does not exist: {dir_path}")
        else:
            if os.path.exists(path):
                return path
            print(f"The folder does not exist: {path}")

def get_valid_interval():
    while True:
        try:
            interval = int(input("Enter synchronization interval in seconds: "))
            if interval > 0:
                return interval
            print("Interval must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("source", nargs="?", help="Path to the source folder")
    parser.add_argument("replica", nargs="?", help="Path to the replica folder")
    parser.add_argument("interval", nargs="?", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", nargs="?", help="Path to the log file")
    
    args = parser.parse_args()
    
    if not args.source or not os.path.exists(args.source):
        args.source = get_valid_path("Error: Enter valid path to source folder: ")
    
    if not args.replica:
        args.replica = get_valid_path("Error: Enter valid path to replica folder: ")
    
    if not args.interval:
        args.interval = get_valid_interval()
    
    if not args.log_file or not os.path.exists(os.path.dirname(args.log_file)):
        args.log_file = get_valid_path("Error: Enter valid path to log file: ", is_file=True)
    
    return args

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Source folder: {args.source}")
    print(f"Replica folder: {args.replica}")
    print(f"Sync interval: {args.interval} seconds")
    print(f"Log file: {args.log_file}")
