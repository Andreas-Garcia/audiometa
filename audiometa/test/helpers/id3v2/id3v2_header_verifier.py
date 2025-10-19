"""ID3 metadata header verification utilities."""

from pathlib import Path


class ID3HeaderVerifier:
    """Utilities for verifying ID3 metadata headers in audio files."""
    
    @staticmethod
    def has_id3v2_header(file_path: Path) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False