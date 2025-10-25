"""RIFF metadata inspection utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class RIFFMetadataGetter:
    """Utilities for inspecting RIFF metadata in audio files."""
    
    @staticmethod
    def get_raw_metadata(file_path: Path) -> Dict[str, Any]:
        """Inspect RIFF metadata using ffprobe, which supports non-standard fields like IAAR."""
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_format', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    
    @staticmethod
    def get_title(file_path: Path) -> str:
        """Get the TITLE chunk from RIFF metadata."""
        result = subprocess.run(
            ['exiftool', '-TITLE', '-s3', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    