"""Vorbis metadata inspection utilities for testing audio file metadata."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class VorbisMetadataGetter:
    
    @staticmethod
    def get_raw_metadata(file_path: Path) -> Dict[str, Any]:
        result = subprocess.run(
            ['metaflac', '--list', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    
    @staticmethod
    def get_title(file_path: Path) -> str:
        result = subprocess.run(
            ['metaflac', '--show-tag=TITLE', str(file_path)],
            capture_output=True, text=True, check=True
        )
        # Output is like "TITLE=Song Title\n"
        lines = result.stdout.strip().split('\n')
        if lines and '=' in lines[0]:
            return lines[0].split('=', 1)[1]
        return ""
    