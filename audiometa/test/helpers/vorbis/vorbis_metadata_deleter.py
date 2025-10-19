"""Vorbis metadata deletion operations."""

from pathlib import Path
from .metaflac_tool import MetaflacTool


class VorbisMetadataDeleter:
    """Static utility class for Vorbis metadata deletion using external metaflac tool."""
    
    @staticmethod
    def delete_comment(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "COMMENT")
    
    @staticmethod
    def delete_title(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "TITLE")
    
    @staticmethod
    def delete_artist(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "ARTIST")
    
    @staticmethod
    def delete_album(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "ALBUM")
    
    @staticmethod
    def delete_genre(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "GENRE")
    
    @staticmethod
    def delete_lyrics(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "LYRICS")
    
    @staticmethod
    def delete_language(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "LANGUAGE")
    
    @staticmethod
    def delete_bpm(file_path: Path) -> None:
        MetaflacTool.delete_tag(file_path, "BPM")