"""Vorbis metadata inspection utilities for testing audio file metadata."""

import subprocess
import re
from pathlib import Path
from typing import Dict, Any


class VorbisMetadataInspector:
    """Utilities for inspecting Vorbis comment metadata in audio files."""
    
    @staticmethod
    def inspect_multiple_entries_in_raw_data(file_path: Path, tag_name: str) -> Dict[str, Any]:
        """Inspect multiple entries in raw Vorbis comments using external tools.
        
        Args:
            file_path: Path to the audio file
            tag_name: The Vorbis comment tag name to check (e.g., 'ARTIST', 'ALBUM', 'COMPOSER')
        
        Returns:
            Dictionary with inspection results including:
            - actual_count: Number of entries found
            - has_multiple: Whether multiple entries exist
            - raw_output: Raw metaflac output
            - entries: List of individual entries found
        """
        result = subprocess.run(
            ['metaflac', '--list', str(file_path)],
            capture_output=True, text=True, check=True
        )
        raw_output = result.stdout
        
        # Case-insensitive search for occurrences of TAG= in the metaflac output.
        # metaflac often prints lines like: "comment[0]: artist=Artist One"
        pattern = re.compile(rf"{re.escape(tag_name)}=(.*)", re.IGNORECASE)
        entries = []
        for line in raw_output.split('\n'):
            m = pattern.search(line)
            if m:
                # Store the full key=value form as seen (lower/upper preserved in output)
                entries.append(m.group(0).strip())

        actual_count = len(entries)
        has_multiple = actual_count > 1
        
        return {
            'actual_count': actual_count,
            'has_multiple': has_multiple,
            'raw_output': raw_output,
            'entries': entries,
            'tag_name': tag_name
        }