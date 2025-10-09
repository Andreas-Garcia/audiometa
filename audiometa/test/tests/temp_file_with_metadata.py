"""Temporary file with metadata utilities for testing.

This module provides utilities for creating temporary test files with specific
metadata configurations, with automatic cleanup support.
"""

from pathlib import Path
from ._internal_test_helpers import create_test_file_with_metadata


class TempFileWithMetadata:
    """Context manager for test files with automatic cleanup.
    
    This class provides a clean way to create temporary test files with
    specific metadata and ensures they are automatically cleaned up when
    the context exits, even if an exception occurs.
    
    Example:
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
                # Use test_file for testing
                update_file_metadata(test_file, new_metadata)
            # File is automatically cleaned up here
        """
    
    def __init__(self, metadata: dict, format_type: str):
        """Initialize the context manager.
        
        Args:
            metadata: Dictionary of metadata to set on the test file
            format_type: Audio format ('mp3', 'flac', 'wav')
        """
        self.metadata = metadata
        self.format_type = format_type
        self.test_file = None
    
    def __enter__(self) -> Path:
        """Create the test file and return its path.
        
        Returns:
            Path to the created test file with metadata
        """
        self.test_file = create_test_file_with_metadata(self.metadata, self.format_type)
        return self.test_file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()


