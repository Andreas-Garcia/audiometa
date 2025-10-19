"""ID3v2 and ID3v1 metadata deletion operations."""

from pathlib import Path
from .mid3v2_tool import Mid3v2Tool
from .id3v2_tool import Id3v2Tool


class ID3v2MetadataDeleter:
    """Static utility class for ID3v2 metadata deletion using external tools."""
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        """Delete ID3v2 comment using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "COMM")
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        """Delete ID3v2 title using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TIT2")
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        """Delete ID3v2 artist using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TPE1")
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        """Delete ID3v2 album using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TALB")
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        """Delete ID3v2 genre using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TCON")
    
    @staticmethod
    def delete_lyrics(file_path: Path) -> None:
        """Delete ID3v2 lyrics using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "USLT")
    
    @staticmethod
    def delete_language(file_path: Path) -> None:
        """Delete ID3v2 language using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TLAN")
    
    @staticmethod
    def delete_bpm(file_path: Path) -> None:
        """Delete ID3v2 BPM using mid3v2 tool."""
        Mid3v2Tool.delete_frame(file_path, "TBPM")


class ID3v1MetadataDeleter:
    """Static utility class for ID3v1 metadata deletion using external tools."""
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        """Delete ID3v1 comment using id3v2 tool."""
        ID3v1MetadataDeleter.delete_comment(file_path)
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        """Delete ID3v1 title using id3v2 tool."""
        ID3v1MetadataDeleter.delete_title(file_path)
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        """Delete ID3v1 artist using id3v2 tool."""
        ID3v1MetadataDeleter.delete_artist(file_path)
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        """Delete ID3v1 album using id3v2 tool."""
        ID3v1MetadataDeleter.delete_album(file_path)
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        """Delete ID3v1 genre using id3v2 tool."""
        ID3v1MetadataDeleter.delete_genre(file_path)