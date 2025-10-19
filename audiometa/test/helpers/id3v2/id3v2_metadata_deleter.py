"""ID3v2 metadata deletion operations."""

from pathlib import Path
from .mid3v2_tool import Mid3v2Tool


class ID3v2MetadataDeleter:
    """Static utility class for ID3v2 metadata deletion using external tools."""
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "COMM")
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TIT2")
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TPE1")
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TALB")
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TCON")
    
    @staticmethod
    def delete_lyrics(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "USLT")
    
    @staticmethod
    def delete_language(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TLAN")
    
    @staticmethod
    def delete_bpm(file_path: Path) -> None:
        Mid3v2Tool.delete_frame(file_path, "TBPM")