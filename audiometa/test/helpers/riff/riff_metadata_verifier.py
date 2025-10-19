"""RIFF metadata verification utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class RIFFMetadataVerifier:
    """Utilities for verifying RIFF metadata in audio files."""
    
    # Mapping from RIFF chunk IDs to exiftool display names
    RIFF_TAG_TO_EXIFTOOL_NAME = {
        'IART': 'Artist',
        'INAM': 'Title', 
        'IGNR': 'Genre',
        'ICMT': 'Comment',
        'ICOP': 'Copyright',
        'IENG': 'Engineer',
        'IMED': 'Medium',
        'IPRD': 'Product',
        'ISBJ': 'Subject',
        'ISFT': 'Software',
        'ISRC': 'Source',
        'ICRD': 'Date Created',
        'ICMP': 'Composer',
        'IKEY': 'Keywords',
        'ILNG': 'Language',
        'IAAR': 'Album Artist',  # Custom field
    }
    
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
            
            # Map RIFF chunk ID to exiftool display name
            display_name = RIFFMetadataVerifier.RIFF_TAG_TO_EXIFTOOL_NAME.get(tag_name, tag_name)
            
            # Count occurrences of the tag - RIFF tags appear as [RIFF] DisplayName
            # Note: exiftool output has variable spacing, so we need to be flexible
            lines = raw_output.split('\n')
            matching_lines = []
            for line in lines:
                # Look for lines that start with [RIFF] and contain our display name
                if line.startswith('[RIFF]') and display_name in line:
                    # Make sure it's the actual field name, not part of a value
                    # Format is: [RIFF]<spaces>FieldName<spaces>: Value
                    parts = line.split(':', 1)
                    if len(parts) >= 1:
                        field_part = parts[0].strip()
                        if field_part.endswith(display_name):
                            matching_lines.append(line)
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