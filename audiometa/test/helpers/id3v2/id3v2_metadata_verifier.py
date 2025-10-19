"""ID3v2 metadata verification utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class ID3v2MetadataVerifier:
    """Utilities for verifying ID3v2 metadata in audio files."""
    
    @staticmethod
    def get_metadata_info(file_path: Path) -> str:
        """Get metadata info using mid3v2 -l command."""
        result = subprocess.run(
            ['mid3v2', '-l', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    
    @staticmethod
    def verify_multiple_entries_in_raw_data(file_path: Path, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw ID3v2 data using external tools.
        
        This method works for all ID3v2 versions (2.3, 2.4) since mid3v2 can read both.
        Note: Will detect multiple entries even in ID3v2.3 files where they're not 
        officially supported but may exist due to malformed files, manual editing, 
        or format conversion artifacts.
        
        Args:
            file_path: Path to the audio file
            tag_name: The ID3v2 tag name to check (e.g., 'TPE1', 'TPE2', 'TCOM')
            expected_count: Expected number of entries. If None, just checks if multiple exist.
        
        Returns:
            Dictionary with verification results including:
            - success: Whether the verification succeeded
            - actual_count: Number of entries found (includes non-compliant duplicates)
            - has_multiple: Whether multiple entries exist
            - raw_output: Raw mid3v2 output
            - entries: List of individual entries found
        """
        try:
            result = subprocess.run(
                ['mid3v2', '-l', str(file_path)],
                capture_output=True, text=True, check=True
            )
            raw_output = result.stdout
            
            # Count occurrences of the tag
            tag_pattern = f"{tag_name}="
            actual_count = raw_output.count(tag_pattern)
            has_multiple = actual_count > 1
            
            # Extract individual entries
            entries = []
            for line in raw_output.split('\n'):
                if line.strip().startswith(tag_pattern):
                    entries.append(line.strip())
            
            # Check if expected count matches
            count_matches = expected_count is None or actual_count == expected_count
            
            return {
                'success': True,
                'actual_count': actual_count,
                'has_multiple': has_multiple,
                'count_matches': count_matches,
                'raw_output': raw_output,
                'entries': entries,
                'tag_name': tag_name
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return {
                'success': False,
                'error': str(e),
                'actual_count': 0,
                'has_multiple': False,
                'count_matches': False,
                'raw_output': '',
                'entries': [],
                'tag_name': tag_name
            }