import os
import hashlib
import shutil

def list_files_and_directories(folder_path):
    """List all files and directories in the given folder."""
    try:
        return os.listdir(folder_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    except PermissionError:
        raise PermissionError(f"Permission denied to access '{folder_path}'.")

def get_file_md5(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_files(file1, file2, method='md5'):
    """Compare two files using modification time or MD5 hash."""
    if method == 'mtime':
        return os.path.getmtime(file1) == os.path.getmtime(file2)
    elif method == 'md5':
        return get_file_md5(file1) == get_file_md5(file2)
    else:
        raise ValueError("Invalid comparison method. Use 'mtime' or 'md5'.")

def copy_files_and_directories(src, dest):
    """Copy files and directories from src to dest."""
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
    except FileNotFoundError:
        raise FileNotFoundError(f"The source '{src}' does not exist.")
    except PermissionError:
        raise PermissionError(f"Permission denied to access '{src}' or '{dest}'.")

def remove_files_and_directories(path):
    """Remove files and directories."""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The path '{path}' does not exist.")
    except PermissionError:
        raise PermissionError(f"Permission denied to remove '{path}'.")