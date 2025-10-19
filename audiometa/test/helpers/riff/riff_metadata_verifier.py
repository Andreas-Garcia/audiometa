"""RIFF metadata verification utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class RIFFMetadataVerifier:
    """Utilities for verifying RIFF metadata in audio files."""
    
    @staticmethod
    def verify_multiple_entries_in_raw_data(file_path: Path, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw RIFF data using external tools.
        
        Args:
            file_path: Path to the audio file
            tag_name: The RIFF chunk name to check (e.g., 'IART', 'IGNR', 'INAM')
            expected_count: Expected number of entries. If None, just checks if multiple exist.
        
        Returns:
            Dictionary with verification results including:
            - success: Whether the verification succeeded
            - actual_count: Number of entries found
            - has_multiple: Whether multiple entries exist
            - raw_output: Raw output from inspection tool
            - entries: List of individual entries found
        """
        try:
            # Use exiftool to inspect RIFF metadata
            result = subprocess.run(
                ['exiftool', '-a', '-G', str(file_path)],
                capture_output=True, text=True, check=True
            )
            raw_output = result.stdout
            
            # Count occurrences of the tag - RIFF tags appear as [RIFF] TagName
            tag_pattern = f"[RIFF] {tag_name}"
            lines = raw_output.split('\n')
            matching_lines = [line for line in lines if tag_pattern in line]
            actual_count = len(matching_lines)
            has_multiple = actual_count > 1
            
            # Check if expected count matches
            count_matches = expected_count is None or actual_count == expected_count
            
            return {
                'success': True,
                'actual_count': actual_count,
                'has_multiple': has_multiple,
                'count_matches': count_matches,
                'raw_output': raw_output,
                'entries': matching_lines,
                'tag_name': tag_name
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fallback: Basic check indicating limited support
            return {
                'success': False,
                'error': f'exiftool not available for RIFF verification: {e}',
                'actual_count': 0,
                'has_multiple': False,
                'count_matches': False,
                'raw_output': '',
                'entries': [],
                'tag_name': tag_name
            }