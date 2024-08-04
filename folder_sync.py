import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    
    args = parser.parse_args()
    
    # Validate paths
    if not os.path.exists(args.source):
        raise ValueError(f"Source folder does not exist: {args.source}")
    if not os.path.exists(os.path.dirname(args.log_file)):
        raise ValueError(f"Log file directory does not exist: {os.path.dirname(args.log_file)}")
    
    return args

if __name__ == "__main__":
    try:
        args = parse_arguments()
        print(f"Source folder: {args.source}")
        print(f"Replica folder: {args.replica}")
        print(f"Sync interval: {args.interval} seconds")
        print(f"Log file: {args.log_file}")
    except Exception as e:
        print(f"Error: {str(e)}")