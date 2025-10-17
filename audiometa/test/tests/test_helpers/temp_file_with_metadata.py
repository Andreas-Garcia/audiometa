"""Consolidated temporary file with metadata utilities for testing.

This module provides a unified TempFileWithMetadata class that combines
file management, external tool operations, and metadata verification
in a single, clean API.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

from .._internal_test_helpers import create_test_file_with_metadata


class TempFileWithMetadata:
    """Context manager for test files with comprehensive metadata operations.
    
    This class provides a unified interface for:
    - Creating temporary test files with metadata
    - Performing external tool operations
    - Verifying metadata and headers
    - Automatic cleanup
    
    Example:
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set additional metadata using external tools
            test_file.set_id3v1_genre("17")
            test_file.set_id3v2_genre("Rock")
            
            # Verify headers
            assert test_file.has_id3v2_header()
            
            # Use test_file.path for testing
            metadata = get_merged_unified_metadata(test_file.path)
    """
    
    def __init__(self, metadata: dict, format_type: str):
        """Initialize the context manager.
        
        Args:
            metadata: Dictionary of metadata to set on the test file
            format_type: Audio format ('mp3', 'id3v1', 'flac', 'wav')
        """
        self.metadata = metadata
        self.format_type = format_type
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
        """Create the test file and return the manager instance.
        
        Returns:
            The TempFileWithMetadata instance for method access
        """
        self.test_file = create_test_file_with_metadata(self.metadata, self.format_type)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test file when exiting the context.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if self.test_file and self.test_file.exists():
            self.test_file.unlink()
    
    # =============================================================================
    # External Tool Operations (previously in script helpers)
    # =============================================================================
    
    def _get_scripts_dir(self) -> Path:
        """Get the scripts directory path."""
        return Path(__file__).parent.parent.parent / "data" / "scripts"
    
    def _run_script(self, script_name: str, check: bool = True) -> subprocess.CompletedProcess:
        """Run an external script with proper error handling."""
        scripts_dir = self._get_scripts_dir()
        script_path = scripts_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        if not script_path.is_file():
            raise FileNotFoundError(f"Script is not a file: {script_path}")
        
        # Make script executable
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                [str(script_path), str(self.test_file)],
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Script {script_name} failed: {e.stderr}") from e
    
    def _run_external_tool(self, command: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run an external tool with proper error handling."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"External tool failed: {e}") from e
    
    # ID3v1 Operations
    def set_id3v1_genre(self, genre_code: str):
        """Set ID3v1 genre using external id3v2 tool."""
        command = [
            "id3v2", "--id3v1-only", 
            f"--genre={genre_code}",
            str(self.test_file)
        ]
        return self._run_external_tool(command)
    
    def set_id3v1_max_metadata(self):
        """Set maximum ID3v1 metadata using external script."""
        return self._run_script("set-id3v1-max-metadata.sh")
    
    def remove_id3v1_metadata(self):
        """Remove ID3v1 metadata using external script."""
        return self._run_script("remove_id3.py")
    
    # ID3v2 Operations
    def set_id3v2_genre(self, genre: str):
        """Set ID3v2 genre using external mid3v2 tool."""
        command = ["mid3v2", "--genre", genre, str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_multiple_genres(self, genres: list[str]):
        """Set ID3v2 multiple genres using external mid3v2 tool."""
        genre_string = "; ".join(genres)
        command = ["mid3v2", "--genre", genre_string, str(self.test_file)]
        return self._run_external_tool(command)
    
    def set_id3v2_max_metadata(self):
        """Set maximum ID3v2 metadata using external script."""
        return self._run_script("set-id3v2-max-metadata.sh")
    
    def remove_id3v2_metadata(self):
        """Remove ID3v2 metadata using external script."""
        return self._run_script("remove_id3.py")
    
    # Vorbis Operations
    def set_vorbis_max_metadata(self):
        """Set maximum Vorbis metadata using external script."""
        return self._run_script("set-vorbis-max-metadata.sh")
    
    def set_vorbis_artists_one_two_three(self):
        """Set specific artists metadata using external script."""
        return self._run_script("set-artists-One-Two-Three-vorbis.sh")
    
    # RIFF Operations
    def set_riff_max_metadata(self):
        """Set maximum RIFF metadata using external script."""
        return self._run_script("set-riff-max-metadata.sh")
    
    def set_riff_genre_text(self, genre_text: str):
        """Set RIFF genre using external exiftool or bwfmetaedit tool."""
        try:
            # Try exiftool first
            command = [
                "exiftool", "-overwrite_original", 
                f"-Genre={genre_text}",
                str(self.test_file)
            ]
            return self._run_external_tool(command)
        except RuntimeError:
            try:
                # Fallback to bwfmetaedit
                command = [
                    "bwfmetaedit", f"--IGNR={genre_text}", str(self.test_file)
                ]
                return self._run_external_tool(command)
            except RuntimeError as e:
                raise RuntimeError(f"Failed to set RIFF genre: {e}") from e
    
    def remove_riff_metadata(self):
        """Remove RIFF metadata using external script."""
        return self._run_script("remove_riff.py")
    
    # =============================================================================
    # Header Detection and Verification (previously in temp_file_with_metadata)
    # =============================================================================
    
    def has_id3v2_header(self) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes.
        
        Returns:
            True if ID3v2 header is present, False otherwise
        """
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
    
    def has_id3v1_header(self) -> bool:
        """Check if file has ID3v1 header by reading the last 128 bytes.
        
        Returns:
            True if ID3v1 header is present, False otherwise
        """
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes
                header = f.read(128)
                return header[:3] == b'TAG'
        except (IOError, OSError):
            return False
    
    def has_vorbis_comments(self) -> bool:
        """Check if file has Vorbis comments using metaflac.
        
        Returns:
            True if Vorbis comments are present, False otherwise
        """
        if not self.test_file:
            return False
        try:
            result = subprocess.run(
                ['metaflac', '--list', str(self.test_file)],
                capture_output=True, text=True, check=True
            )
            return 'VORBIS_COMMENT' in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def has_riff_info_chunk(self) -> bool:
        """Check if file has RIFF INFO chunk by reading file structure.
        
        Returns:
            True if RIFF INFO chunk is present, False otherwise
        """
        if not self.test_file:
            return False
        try:
            with open(self.test_file, 'rb') as f:
                # Read first few bytes to check for ID3v2 tags
                first_bytes = f.read(10)
                f.seek(0)  # Reset to beginning
                
                if first_bytes.startswith(b'ID3'):
                    # File has ID3v2 tags, find RIFF header after them
                    data = f.read()
                    pos = 0
                    while pos < len(data) - 8:
                        if data[pos:pos+4] == b'RIFF':
                            # Found RIFF header, check for LIST chunk containing INFO
                            riff_size = int.from_bytes(data[pos+4:pos+8], 'little')
                            riff_data = data[pos+8:pos+8+riff_size]
                            
                            # Search for LIST chunk containing INFO in RIFF data
                            # Skip the WAVE chunk header (4 bytes)
                            info_pos = 4
                            while info_pos < len(riff_data) - 8:
                                chunk_id = riff_data[info_pos:info_pos+4]
                                chunk_size = int.from_bytes(riff_data[info_pos+4:info_pos+8], 'little')
                                
                                if chunk_id == b'LIST':
                                    # Check if this LIST chunk contains INFO
                                    list_data = riff_data[info_pos+8:info_pos+8+chunk_size]
                                    if len(list_data) >= 4 and list_data[:4] == b'INFO':
                                        return True
                                
                                # Move to next chunk (chunk size + padding)
                                info_pos += 8 + chunk_size
                                if chunk_size % 2 == 1:  # Odd size needs padding
                                    info_pos += 1
                            return False
                        pos += 1
                    return False
                else:
                    # File starts with RIFF header
                    riff_header = f.read(12)
                    if riff_header[:4] != b'RIFF':
                        return False
                    
                    # Look for LIST chunk containing INFO
                    chunk_size = int.from_bytes(riff_header[4:8], 'little')
                    data = f.read(chunk_size)
                    
                    # Search for LIST chunk containing INFO
                    pos = 0
                    while pos < len(data) - 8:
                        chunk_id = data[pos:pos+4]
                        chunk_size = int.from_bytes(data[pos+4:pos+8], 'little')
                        
                        if chunk_id == b'LIST':
                            # Check if this LIST chunk contains INFO
                            list_data = data[pos+8:pos+8+chunk_size]
                            if len(list_data) >= 4 and list_data[:4] == b'INFO':
                                return True
                        
                        # Move to next chunk (chunk size + padding)
                        pos += 8 + chunk_size
                        if chunk_size % 2 == 1:  # Odd size needs padding
                            pos += 1
                    
                    return False
        except (IOError, OSError, ValueError):
            return False
    
    def get_metadata_headers_present(self) -> Dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file.
        
        Returns:
            Dictionary with format names as keys and boolean presence as values
        """
        if not self.test_file:
            return {}
        return {
            'id3v2': self.has_id3v2_header(),
            'id3v1': self.has_id3v1_header(),
            'vorbis': self.has_vorbis_comments(),
            'riff': self.has_riff_info_chunk()
        }
    
    def verify_headers_removed(self, expected_removed: list[str] = None) -> Dict[str, bool]:
        """Verify that specified metadata headers have been removed.
        
        Args:
            expected_removed: List of format names that should be removed.
                             If None, checks all formats.
        
        Returns:
            Dictionary with format names as keys and removal status as values
        """
        if not self.test_file:
            return {}
        if expected_removed is None:
            expected_removed = ['id3v2', 'id3v1', 'vorbis', 'riff']
        
        headers_present = self.get_metadata_headers_present()
        
        return {
            format_name: not headers_present.get(format_name, False)
            for format_name in expected_removed
        }
    
    def check_metadata_with_external_tools(self) -> Dict[str, Any]:
        """Check metadata using external tools for comprehensive verification.
        
        Returns:
            Dictionary with tool results
        """
        if not self.test_file:
            return {}
        results = {}
        
        # Check with mid3v2
        try:
            result = subprocess.run(
                ['mid3v2', '-l', str(self.test_file)],
                capture_output=True, text=True, check=True
            )
            results['mid3v2'] = {
                'success': True,
                'output': result.stdout,
                'has_id3v2': 'ID3v2 tag' in result.stdout and 'No ID3v2 tag found' not in result.stdout,
                'has_id3v1': 'ID3v1 tag' in result.stdout and 'No ID3v1 tag found' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mid3v2'] = {'success': False, 'error': str(e)}
        
        # Check with mutagen-inspect
        try:
            result = subprocess.run(
                ['mutagen-inspect', str(self.test_file)],
                capture_output=True, text=True, check=True
            )
            results['mutagen_inspect'] = {
                'success': True,
                'output': result.stdout,
                'has_metadata': 'No tags' not in result.stdout
            }
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            results['mutagen_inspect'] = {'success': False, 'error': str(e)}
        
        # Check with metaflac (for FLAC files)
        if self.test_file.suffix.lower() == '.flac':
            try:
                result = subprocess.run(
                    ['metaflac', '--list', str(self.test_file)],
                    capture_output=True, text=True, check=True
                )
                results['metaflac'] = {
                    'success': True,
                    'output': result.stdout,
                    'has_vorbis': 'VORBIS_COMMENT' in result.stdout
                }
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                results['metaflac'] = {'success': False, 'error': str(e)}
        
        return results
