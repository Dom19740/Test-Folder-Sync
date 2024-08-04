import unittest
import os
import shutil
from unittest.mock import patch
from folder_sync import sync_folders
from logging_setup import setup_logging

class TestFolderSyncErrorHandling(unittest.TestCase):

    def setUp(self):
        # Create temporary directories for testing
        self.source = 'test_source'
        self.replica = 'test_replica'
        os.makedirs(self.source, exist_ok=True)
        os.makedirs(self.replica, exist_ok=True)
        self.logger = setup_logging('test_log.log')

    def tearDown(self):
        # Remove temporary directories after tests
        shutil.rmtree(self.source)
        shutil.rmtree(self.replica)
        if os.path.exists('test_log.log'):
            os.remove('test_log.log')

    def test_permission_error(self):
        # Create a file in the source directory
        source_file = os.path.join(self.source, 'test_file.txt')
        with open(source_file, 'w') as f:
            f.write('This is a test file.')

        # Make the replica directory read-only
        os.chmod(self.replica, 0o400)

        # Run synchronization and check for permission error
        with self.assertLogs(self.logger, level='ERROR') as log:
            sync_folders(self.source, self.replica, self.logger)
            self.assertTrue(any('Permission error' in message for message in log.output))

        # Restore permissions
        os.chmod(self.replica, 0o700)

    def test_file_not_found_error(self):
        # Create a file in the source directory
        source_file = os.path.join(self.source, 'test_file.txt')
        with open(source_file, 'w') as f:
            f.write('This is a test file.')

        # Remove the file to simulate FileNotFoundError
        os.remove(source_file)

        # Run synchronization and check for file not found error
        with self.assertLogs(self.logger, level='ERROR') as log:
            sync_folders(self.source, self.replica, self.logger)
            self.assertTrue(any('File not found' in message for message in log.output))

    @patch('folder_sync.copy_files_and_directories', side_effect=Exception('Test exception'))
    def test_general_exception(self, mock_copy):
        # Create a file in the source directory
        source_file = os.path.join(self.source, 'test_file.txt')
        with open(source_file, 'w') as f:
            f.write('This is a test file.')

        # Run synchronization and check for general exception
        with self.assertLogs(self.logger, level='ERROR') as log:
            sync_folders(self.source, self.replica, self.logger)
            self.assertTrue(any('Error during synchronization' in message for message in log.output))

if __name__ == '__main__':
    unittest.main()