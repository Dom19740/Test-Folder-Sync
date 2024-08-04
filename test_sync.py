import unittest
import shutil
import os
import logging
from logging_setup import setup_logging  # Adjust the import as necessary

class TestFolderSyncErrorHandling(unittest.TestCase):

    def setUp(self):
        self.source = 'test_source'
        self.destination = 'test_destination'
        os.makedirs(self.source, exist_ok=True)
        os.makedirs(self.destination, exist_ok=True)
        
        # Setup logging
        self.log_file = 'test_log.log'
        self.logger = setup_logging(self.log_file)
        self.log_capture = logging.getLogger('folder_sync')
        self.log_capture.setLevel(logging.DEBUG)
        self.log_capture_handler = logging.StreamHandler()
        self.log_capture_handler.setFormatter(logging.Formatter('%(message)s'))
        self.log_capture.addHandler(self.log_capture_handler)
        self.log_capture_output = []

        def capture_log(record):
            self.log_capture_output.append(record.getMessage())

        self.log_capture_handler.emit = capture_log

    def tearDown(self):
        shutil.rmtree(self.source, ignore_errors=True)
        shutil.rmtree(self.destination, ignore_errors=True)
        
        # Remove log handlers and close the log file
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
        
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_file_not_found_error(self):
        # Simulate file not found error
        try:
            os.remove(os.path.join(self.source, 'non_existent_file.txt'))
        except FileNotFoundError as e:
            self.logger.error('File not found: %s', e)

        self.assertTrue(any('File not found' in message for message in self.log_capture_output))

    def test_permission_error(self):
        # Simulate permission error by changing file permissions to read-only
        test_file_path = os.path.join(self.source, 'test_file.txt')
        with open(test_file_path, 'w') as f:
            f.write('test')
        
        # Change the file permissions to read-only
        os.chmod(test_file_path, 0o444)
        
        try:
            with open(test_file_path, 'w') as f2:
                f2.write('test')
        except PermissionError as e:
            self.logger.error('Permission error: %s', e)

        self.assertTrue(any('Permission error' in message for message in self.log_capture_output))
        
    def test_general_exception(self):
        # Simulate general exception
        try:
            raise Exception('General error')
        except Exception as e:
            self.logger.error('General exception: %s', e)

        self.assertTrue(any('General exception' in message for message in self.log_capture_output))

if __name__ == '__main__':
    unittest.main()