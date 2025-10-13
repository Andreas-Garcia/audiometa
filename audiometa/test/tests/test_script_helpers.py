"""Helper functions for using external scripts in tests.

This module provides Python functions that call the external scripts
in audiometa/test/data/scripts/ to set up test files with metadata
without using the app's own update functions. This prevents circular
dependencies in tests where writing logic could mask reading bugs.
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class ScriptHelper:
    
    def __init__(self, scripts_dir: Optional[Path] = None):
        if scripts_dir is None:
            # Default to the scripts directory relative to this file
            self.scripts_dir = Path(__file__).parent.parent / "data" / "scripts"
        else:
            self.scripts_dir = scripts_dir
    
    def _run_script(self, script_name: str, file_path: Path, check: bool = True) -> subprocess.CompletedProcess:
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        if not script_path.is_file():
            raise FileNotFoundError(f"Script is not a file: {script_path}")
        
        # Make script executable
        script_path.chmod(0o755)
        
        try:
            result = subprocess.run(
                [str(script_path), str(file_path)],
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Script {script_name} failed: {e.stderr}") from e
    
    def set_id3v2_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-id3v2-max-metadata.sh", file_path)
    
    def set_vorbis_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-vorbis-max-metadata.sh", file_path)
    
    def set_riff_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-riff-max-metadata.sh", file_path)
    
    def set_id3v1_max_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-id3v1-max-metadata.sh", file_path)
    
    def set_artists_one_two_three_vorbis(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("set-artists-One-Two-Three-vorbis.sh", file_path)
    
    def remove_id3_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("remove_id3.py", file_path)
    
    def remove_riff_metadata(self, file_path: Path) -> subprocess.CompletedProcess:
        return self._run_script("remove_riff.py", file_path)
    
    # Header Detection Methods
    
    def has_id3v2_header(self, file_path: Path) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if ID3v2 header is present, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
    
    def has_id3v1_header(self, file_path: Path) -> bool:
        """Check if file has ID3v1 header by reading the last 128 bytes.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if ID3v1 header is present, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes
                header = f.read(128)
                return header[:3] == b'TAG'
        except (IOError, OSError):
            return False
    
    def has_vorbis_comments(self, file_path: Path) -> bool:
        """Check if file has Vorbis comments using metaflac.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if Vorbis comments are present, False otherwise
        """
        try:
            result = subprocess.run(
                ['metaflac', '--list', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return 'VORBIS_COMMENT' in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def has_riff_info_chunk(self, file_path: Path) -> bool:
        """Check if file has RIFF INFO chunk by reading file structure.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if RIFF INFO chunk is present, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                # Read RIFF header
                riff_header = f.read(12)
                if riff_header[:4] != b'RIFF':
                    return False
                
                # Look for INFO chunk
                chunk_size = int.from_bytes(riff_header[4:8], 'little')
                data = f.read(chunk_size)
                
                # Search for INFO chunk
                pos = 0
                while pos < len(data) - 8:
                    chunk_id = data[pos:pos+4]
                    chunk_size = int.from_bytes(data[pos+4:pos+8], 'little')
                    
                    if chunk_id == b'INFO':
                        return True
                    
                    # Move to next chunk (chunk size + padding)
                    pos += 8 + chunk_size
                    if chunk_size % 2 == 1:  # Odd size needs padding
                        pos += 1
                
                return False
        except (IOError, OSError, ValueError):
            return False
    
    def get_metadata_headers_present(self, file_path: Path) -> Dict[str, bool]:
        """Get a comprehensive report of all metadata headers present in the file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with format names as keys and boolean presence as values
        """
        return {
            'id3v2': self.has_id3v2_header(file_path),
            'id3v1': self.has_id3v1_header(file_path),
            'vorbis': self.has_vorbis_comments(file_path),
            'riff': self.has_riff_info_chunk(file_path)
        }
    
    def verify_headers_removed(self, file_path: Path, expected_removed: list[str] = None) -> Dict[str, bool]:
        """Verify that specified metadata headers have been removed.
        
        Args:
            file_path: Path to the audio file
            expected_removed: List of format names that should be removed.
                             If None, checks all formats.
        
        Returns:
            Dictionary with format names as keys and removal status as values
        """
        if expected_removed is None:
            expected_removed = ['id3v2', 'id3v1', 'vorbis', 'riff']
        
        headers_present = self.get_metadata_headers_present(file_path)
        
        return {
            format_name: not headers_present.get(format_name, False)
            for format_name in expected_removed
        }
    
    def check_metadata_with_external_tools(self, file_path: Path) -> Dict[str, Any]:
        """Check metadata using external tools for comprehensive verification.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with tool results
        """
        results = {}
        
        # Check with mid3v2
        try:
            result = subprocess.run(
                ['mid3v2', '-l', str(file_path)],
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
                ['mutagen-inspect', str(file_path)],
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
        if file_path.suffix.lower() == '.flac':
            try:
                result = subprocess.run(
                    ['metaflac', '--list', str(file_path)],
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
