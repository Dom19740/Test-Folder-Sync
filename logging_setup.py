import os
import logging

def setup_logging(log_file):
    logger = logging.getLogger('folder_sync')
    logger.setLevel(logging.DEBUG)

    # Check if log_file is a directory and adjust log_file path
    if os.path.isdir(log_file):
        log_file = os.path.join(log_file, 'sync.log')

    # Ensure the log directory exists and is writable
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        if not os.access(log_dir, os.W_OK):
            raise PermissionError(f"Log directory '{log_dir}' is not writable.")

    # Check if the log file is writable or can be created
    if os.path.exists(log_file) and not os.access(log_file, os.W_OK):
        raise PermissionError(f"Log file '{log_file}' is not writable.")

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file)

    # Set logging level for handlers
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)

    # Create a formatter with timestamps and add it to both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger