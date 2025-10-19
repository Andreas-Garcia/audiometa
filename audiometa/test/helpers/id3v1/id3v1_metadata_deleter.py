"""ID3v1 metadata deletion operations."""

from pathlib import Path
from .id3v1_tool import Id3v1Tool


class ID3v1MetadataDeleter:
    """Static utility class for ID3v1 metadata deletion using external tools."""
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        Id3v1Tool.delete_tag(file_path, "COMM")
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        Id3v1Tool.delete_tag(file_path, "TIT2")
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        Id3v1Tool.delete_tag(file_path, "TPE1")
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        Id3v1Tool.delete_tag(file_path, "TALB")
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        Id3v1Tool.delete_tag(file_path, "TCON")