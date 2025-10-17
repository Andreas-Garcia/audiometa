"""Helper class for ID3v1 metadata operations using external tools."""

from pathlib import Path
from .base_helper import BaseHelper


class Id3v1Helper(BaseHelper):
    """Helper class for ID3v1 metadata operations."""
    
    @staticmethod
    def set_max_metadata(file_path: Path):
        """Set maximum ID3v1 metadata using external script."""
        return Id3v1Helper._run_script("set-id3v1-max-metadata.sh", file_path)
    
    @staticmethod
    def set_genre(file_path: Path, genre_code: str):
        """Set ID3v1 genre using external id3v2 tool."""
        command = [
            "id3v2", "--id3v1-only", 
            f"--genre={genre_code}",
            str(file_path)
        ]
        return Id3v1Helper._run_external_tool(command)
    
    @staticmethod
    def remove_metadata(file_path: Path):
        """Remove ID3v1 metadata using external script."""
        return Id3v1Helper._run_script("remove_id3.py", file_path)
    
    @staticmethod
    def has_header(file_path: Path) -> bool:
        """Check if file has ID3v1 header by reading the last 128 bytes."""
        try:
            with open(file_path, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes
                header = f.read(128)
                return header[:3] == b'TAG'
        except (IOError, OSError):
            return False
