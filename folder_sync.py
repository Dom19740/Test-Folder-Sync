import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Folder Synchronization Script')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('log_file', type=str, default='sync.log', help='Path to the log file (default: sync.log)')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    return parser.parse_args()

# Invalid path error handling
def validate_paths(source, replica, log_file):
    paths = [('source', source), ('replica', replica), ('log file', log_file)]
    while any(not os.path.exists(path) for name, path in paths):
        for i, (name, path) in enumerate(paths):
            if not os.path.exists(path):
                paths[i] = (name, input(f"{name.capitalize()} path '{path}' does not exist. Please enter a valid {name} path: "))
    return paths[0][1], paths[1][1], paths[2][1]

# Example usage
args = parse_arguments()
args.source, args.replica, args.log_file = validate_paths(args.source, args.replica, args.log_file)

print(f"Source folder: {args.source}")
print(f"Replica folder: {args.replica}")
print(f"Logs folder: {args.log_file}")
print(f"Sync interval: {args.interval} seconds")