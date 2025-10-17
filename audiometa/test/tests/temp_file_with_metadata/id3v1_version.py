"""ID3v1 version-specific temporary file utilities for testing.

This module provides TempFileWithId3v1Version for creating temporary test files 
with specific ID3v1 version metadata, with automatic cleanup support.
"""

import tempfile
import shutil
from pathlib import Path

from .base import TempFileWithMetadata


class TempFileWithId3v1Version:
    """Context manager for test files with specific ID3v1 version and automatic cleanup."""
    
    def __init__(self, id3v1_version):
        self.id3v1_version = id3v1_version
        self.test_file = None
    
    @property
    def path(self) -> Path:
        """Get the path to the test file."""
        if not self.test_file:
            raise RuntimeError("Test file not created yet. Use within context manager.")
        return self.test_file
    
    def __enter__(self):
        """Create the test file with specific ID3v1 version and return its path."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            self.test_file = Path(tmp_file.name)
        
        # Copy from template file
        template_file = Path(__file__).parent.parent / "data" / "audio_files" / "metadata=none.mp3"
        shutil.copy2(template_file, self.test_file)
        
        # Create comprehensive ID3v1 metadata
        comprehensive_metadata = {
            "title": f"ID3v1.{self.id3v1_version} Test Title",
            "artist": f"ID3v1.{self.id3v1_version} Test Artist",
            "album": f"ID3v1.{self.id3v1_version} Test Album",
            "year": "2023",
            "genre": "Rock",
            "comment": f"ID3v1.{self.id3v1_version} test comment"
        }
        
        # Add track number for ID3v1.1
        if self.id3v1_version == '1.1':
            comprehensive_metadata["track"] = 1
        
        # Use TempFileWithMetadata to create ID3v1 metadata
        with TempFileWithMetadata(comprehensive_metadata, "mp3") as id3v1_file:
            # Copy the file with ID3v1 metadata to our test file
            shutil.copy2(id3v1_file.path, self.test_file)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context."""
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()
    
    def has_id3v1_metadata(self) -> bool:
        """Check if file has ID3v1 metadata by reading the last 128 bytes."""
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes
                tag_data = f.read(128)
                return tag_data[:3] == b'TAG'
        except (IOError, OSError):
            return False
