"""Vorbis multiple metadata manager for creating test files with specific configurations."""

from pathlib import Path
from typing import List

from .metaflac_tool import MetaflacTool


class VorbisMultipleMetadataManager:
    """Static utility class for setting multiple values in Vorbis comment metadata."""
    
    @staticmethod
    def set_multiple_artists(file_path: Path, artists: List[str]):
        """Set multiple Vorbis artists using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "ARTIST", artists)
    
    @staticmethod
    def set_multiple_album_artists(file_path: Path, album_artists: List[str]):
        """Set multiple Vorbis album artists using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "ALBUMARTIST", album_artists)
    
    @staticmethod
    def set_multiple_composers(file_path: Path, composers: List[str]):
        """Set multiple Vorbis composers using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "COMPOSER", composers)
    
    @staticmethod
    def set_multiple_genres(file_path: Path, genres: List[str]):
        """Set multiple Vorbis genres using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "GENRE", genres)
    
    @staticmethod
    def set_multiple_performers(file_path: Path, performers: List[str]):
        """Set multiple Vorbis performers using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "PERFORMER", performers)
    
    @staticmethod
    def set_multiple_comments(file_path: Path, comments: List[str]):
        """Set multiple Vorbis comments using external metaflac tool."""
        MetaflacTool.set_multiple_tags(file_path, "COMMENT", comments)