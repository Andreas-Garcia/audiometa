"""ID3v2 version-specific temporary file utilities for testing.

This module provides TempFileWithId3v2Version for creating temporary test files 
with specific ID3v2 version metadata, with automatic cleanup support.
"""

import tempfile
import shutil
from pathlib import Path

from audiometa import update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TempFileWithId3v2Version:
    """Context manager for test files with specific ID3v2 version and automatic cleanup."""
    
    def __init__(self, id3v2_version):
        self.id3v2_version = id3v2_version
        self.test_file = None
    
    @property
    def path(self) -> Path:
        """Get the path to the test file.
        
        Returns:
            Path to the test file
        """
        if not self.test_file:
            raise RuntimeError("Test file not created yet. Use within context manager.")
        return self.test_file
    
    def __enter__(self):
        """Create the test file with specific ID3v2 version and return its path."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            self.test_file = Path(tmp_file.name)
        
        # Copy from template file
        template_file = Path(__file__).parent.parent / "data" / "audio_files" / "metadata=none.mp3"
        shutil.copy2(template_file, self.test_file)
        
        # Create comprehensive metadata with ID3v2 supported fields only
        comprehensive_metadata = {
            UnifiedMetadataKey.TITLE: "Comprehensive Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Primary Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Comprehensive Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre",
            UnifiedMetadataKey.RELEASE_DATE: "2023",
            UnifiedMetadataKey.COMMENT: "This is a comprehensive test comment"
        }
        
        # Use the library's update_file_metadata function with specific ID3v2 version
        update_file_metadata(self.test_file, comprehensive_metadata, id3v2_version=self.id3v2_version)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context."""
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()
    
    def has_id3v2_header(self) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
    
    def get_metadata_headers_present(self) -> dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file."""
        if not self.test_file:
            return {}
        return {
            'id3v2': self.has_id3v2_header(),
            'id3v1': False,  # We're not testing ID3v1 in this context
            'vorbis': False,  # We're not testing Vorbis in this context
            'riff': False   # We're not testing RIFF in this context
        }
