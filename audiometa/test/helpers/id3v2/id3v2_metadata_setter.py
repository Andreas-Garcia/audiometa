"""ID3v2 and ID3v1 metadata setting operations."""

from pathlib import Path
from typing import List
from .mid3v2_tool import Mid3v2Tool
from .id3v2_tool import Id3v2Tool


class ID3v2MetadataSetter:
    """Static utility class for ID3v2 metadata setting using external tools."""
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set ID3v2 comment using external mid3v2 tool."""
        Mid3v2Tool.set_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        """Set ID3v2 title using external id3v2 tool with --id3v2-only flag."""
        Id3v2Tool.set_id3v2_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        """Set ID3v2 artist using external id3v2 tool with --id3v2-only flag."""
        Id3v2Tool.set_id3v2_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set ID3v2 album using external mid3v2 tool."""
        Mid3v2Tool.set_album(file_path, album)
    
    @staticmethod
    def set_genre(file_path: Path, genre: str) -> None:
        """Set ID3v2 genre using external mid3v2 tool."""
        Mid3v2Tool.set_genre(file_path, genre)
    
    @staticmethod
    def set_lyrics(file_path: Path, lyrics: str) -> None:
        """Set ID3v2 lyrics using external mid3v2 tool."""
        Mid3v2Tool.set_lyrics(file_path, lyrics)
    
    @staticmethod
    def set_language(file_path: Path, language: str) -> None:
        """Set ID3v2 language using external mid3v2 tool."""
        Mid3v2Tool.set_language(file_path, language)
    
    @staticmethod
    def set_bpm(file_path: Path, bpm: int) -> None:
        """Set ID3v2 BPM using external mid3v2 tool."""
        Mid3v2Tool.set_bpm(file_path, bpm)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        """Set maximum ID3v2 metadata using external script."""
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v2-max-metadata.sh", file_path, scripts_dir)


class ID3v1MetadataSetter:
    """Static utility class for ID3v1 metadata setting using external tools."""
    
    @staticmethod
    def set_genre(file_path: Path, genre_code: str) -> None:
        """Set ID3v1 genre using external id3v2 tool."""
        Id3v2Tool.set_id3v1_genre(file_path, genre_code)
    
    @staticmethod
    def set_comment(file_path: Path, comment: str) -> None:
        """Set ID3v1 comment using external id3v2 tool."""
        Id3v2Tool.set_id3v1_comment(file_path, comment)
    
    @staticmethod
    def set_title(file_path: Path, title: str) -> None:
        """Set ID3v1 title using external id3v2 tool."""
        Id3v2Tool.set_id3v1_title(file_path, title)
    
    @staticmethod
    def set_artist(file_path: Path, artist: str) -> None:
        """Set ID3v1 artist using external id3v2 tool."""
        Id3v2Tool.set_id3v1_artist(file_path, artist)
    
    @staticmethod
    def set_album(file_path: Path, album: str) -> None:
        """Set ID3v1 album using external id3v2 tool."""
        Id3v2Tool.set_id3v1_album(file_path, album)
    
    @staticmethod
    def set_max_metadata(file_path: Path) -> None:
        """Set maximum ID3v1 metadata using external script."""
        from ..common.external_tool_runner import run_script
        from pathlib import Path
        scripts_dir = Path(__file__).parent.parent.parent.parent / "test" / "data" / "scripts"
        run_script("set-id3v1-max-metadata.sh", file_path, scripts_dir)