"""Vorbis metadata verification utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class VorbisMetadataVerifier:
    """Utilities for verifying Vorbis comment metadata in audio files."""
    
    @staticmethod
    def verify_multiple_entries_in_raw_data(file_path: Path, tag_name: str, expected_count: int = None) -> Dict[str, Any]:
        """Verify multiple entries exist in raw Vorbis comments using external tools.
        
        Args:
            file_path: Path to the audio file
            tag_name: The Vorbis comment tag name to check (e.g., 'ARTIST', 'ALBUM', 'COMPOSER')
            expected_count: Expected number of entries. If None, just checks if multiple exist.
        
        Returns:
            Dictionary with verification results including:
            - success: Whether the verification succeeded
            - actual_count: Number of entries found
            - has_multiple: Whether multiple entries exist
            - raw_output: Raw metaflac output
            - entries: List of individual entries found
        """
        try:
            result = subprocess.run(
                ['metaflac', '--list', str(file_path)],
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