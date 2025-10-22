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