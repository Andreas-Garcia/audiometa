"""Helper class for ID3v2 metadata operations using external tools."""

from pathlib import Path
from .base_helper import BaseHelper


class Id3v2Helper(BaseHelper):
    """Helper class for ID3v2 metadata operations."""
    
    @staticmethod
    def set_max_metadata(file_path: Path):
        """Set maximum ID3v2 metadata using external script."""
        return Id3v2Helper._run_script("set-id3v2-max-metadata.sh", file_path)
    
    @staticmethod
    def set_genre(file_path: Path, genre: str):
        """Set ID3v2 genre using external mid3v2 tool."""
        command = ["mid3v2", "--genre", genre, str(file_path)]
        return Id3v2Helper._run_external_tool(command)
    
    @staticmethod
    def set_multiple_genres(file_path: Path, genres: list[str]):
        """Set ID3v2 multiple genres using external mid3v2 tool."""
        # Join genres with semicolon separator for mid3v2
        genre_string = "; ".join(genres)
        command = ["mid3v2", "--genre", genre_string, str(file_path)]
        return Id3v2Helper._run_external_tool(command)
    
    @staticmethod
    def remove_metadata(file_path: Path):
        """Remove ID3v2 metadata using external script."""
        return Id3v2Helper._run_script("remove_id3.py", file_path)
    
    @staticmethod
    def has_header(file_path: Path) -> bool:
        """Check if file has ID3v2 header by reading the first 10 bytes."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(10)
                return header[:3] == b'ID3'
        except (IOError, OSError):
            return False
