import unittest
from unittest.mock import patch, Mock
import os
import tempfile
import shutil
import logging
from folder_sync import sync_folders, validate_paths, validate_interval

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestFolderSync(unittest.TestCase):

    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")
        self.source_dir = tempfile.mkdtemp()
        self.replica_dir = tempfile.mkdtemp()
        self.log_dir = tempfile.mkdtemp()

    def tearDown(self):
        logger.info(f"Tearing down test: {self._testMethodName}")
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.replica_dir)
        shutil.rmtree(self.log_dir)

    def test_validate_paths(self):
        logger.info("Running test_validate_paths")
        source, replica, log_file = validate_paths(self.source_dir, self.replica_dir, self.log_dir)
        self.assertEqual(source, self.source_dir)
        self.assertEqual(replica, self.replica_dir)
        self.assertEqual(log_file, self.log_dir)
        logger.info("test_validate_paths passed")

        logger.info("Testing invalid path scenario")
        with patch('builtins.input', return_value=self.source_dir):
            source, _, _ = validate_paths('/invalid/path', self.replica_dir, self.log_dir)
            self.assertEqual(source, self.source_dir)
        logger.info("Invalid path scenario passed")

    def test_validate_interval(self):
        logger.info("Running test_validate_interval")
        self.assertEqual(validate_interval('10'), 10)
        logger.info("Valid interval test passed")

        logger.info("Testing invalid interval scenario")
        with patch('builtins.input', return_value='5'):
            self.assertEqual(validate_interval('invalid'), 5)
        logger.info("Invalid interval scenario passed")

    @patch('folder_sync.copy_files_and_directories')
    @patch('folder_sync.remove_files_and_directories')
    @patch('folder_sync.compare_files')
    def test_sync_folders_normal(self, mock_compare, mock_remove, mock_copy):
        logger.info("Running test_sync_folders_normal")
        mock_compare.return_value = False  # Files are different
        
        open(os.path.join(self.source_dir, 'test_file.txt'), 'w').close()
        
        sync_logger = Mock()
        sync_folders(self.source_dir, self.replica_dir, sync_logger)
        
        mock_copy.assert_called()
        sync_logger.info.assert_called()
        logger.info("test_sync_folders_normal passed")

    @patch('folder_sync.copy_files_and_directories')
    def test_sync_folders_permission_error(self, mock_copy):
        logger.info("Running test_sync_folders_permission_error")
        mock_copy.side_effect = PermissionError("Permission denied")
        
        open(os.path.join(self.source_dir, 'test_file.txt'), 'w').close()
        
        sync_logger = Mock()
        sync_folders(self.source_dir, self.replica_dir, sync_logger)
        
        sync_logger.error.assert_called_with("Permission error: Permission denied")
        logger.info("test_sync_folders_permission_error passed")

    @patch('folder_sync.copy_files_and_directories')
    def test_sync_folders_file_not_found(self, mock_copy):
        logger.info("Running test_sync_folders_file_not_found")
        mock_copy.side_effect = FileNotFoundError("File not found")
        
        open(os.path.join(self.source_dir, 'test_file.txt'), 'w').close()
        
        sync_logger = Mock()
        sync_folders(self.source_dir, self.replica_dir, sync_logger)
        
        sync_logger.error.assert_called_with("File not found: File not found")
        logger.info("test_sync_folders_file_not_found passed")

    @patch('folder_sync.copy_files_and_directories')
    def test_sync_folders_network_error(self, mock_copy):
        logger.info("Running test_sync_folders_network_error")
        mock_copy.side_effect = IOError("Network error")
        
