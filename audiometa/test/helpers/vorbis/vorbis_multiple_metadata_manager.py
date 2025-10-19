"""Vorbis multiple metadata manager for creating test files with specific configurations."""

from pathlib import Path
from typing import List

from .metaflac_tool import MetaflacTool


class VorbisMultipleMetadataManager:
    """Manager for setting multiple values in Vorbis comment metadata."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def set_multiple_artists(self, artists: List[str]):
        """Set Vorbis multiple artists using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "ARTIST", artists)
    
    def set_multiple_album_artists(self, album_artists: List[str]):
        """Set Vorbis multiple album artists using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "ALBUMARTIST", album_artists)
    
    def set_multiple_composers(self, composers: List[str]):
        """Set Vorbis multiple composers using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "COMPOSER", composers)
    
    def set_multiple_genres(self, genres: List[str]):
        """Set Vorbis multiple genres using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "GENRE", genres)
    
    def set_multiple_performers(self, performers: List[str]):
        """Set Vorbis multiple performers using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "PERFORMER", performers)
    
    def set_multiple_comments(self, comments: List[str]):
        """Set Vorbis multiple comments using external metaflac tool."""
        MetaflacTool.set_multiple_tags(self.file_path, "COMMENT", comments)