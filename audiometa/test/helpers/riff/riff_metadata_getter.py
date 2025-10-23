"""RIFF metadata inspection utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class RIFFMetadataGetter:
    """Utilities for inspecting RIFF metadata in audio files."""
    
    @staticmethod
    def get_raw_metadata(file_path: Path) -> Dict[str, Any]:
        """Inspect a specific RIFF chunk in raw metadata using exiftool."""
        result = subprocess.run(
            ['exiftool', '-a', '-G', str(file_path)],
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
    