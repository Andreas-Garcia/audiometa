"""Vorbis metadata header verification utilities."""

import subprocess
from pathlib import Path


class VorbisHeaderVerifier:
    """Utilities for verifying Vorbis metadata headers in audio files."""
    
    @staticmethod
    def has_vorbis_comments(file_path: Path) -> bool:
        """Check if file has Vorbis comments using metaflac."""
        try:
            result = subprocess.run(
                ['metaflac', '--list', str(file_path)],
                capture_output=True, text=True, check=True
            )
            return 'VORBIS_COMMENT' in result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False