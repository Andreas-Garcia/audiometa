"""RIFF multiple metadata manager for creating test files with specific configurations."""

from pathlib import Path
from typing import List

from .bwfmetaedit_tool import BwfmetaeditTool


class RIFFMultipleMetadataManager:
    """Static utility class for setting multiple values in RIFF metadata."""
    
    @staticmethod
    def set_multiple_artists(file_path: Path, artists: List[str]):
        """Set RIFF multiple artists using external tool (creates multiple chunks)."""
        # For testing multiple instances, we'd need to use a more sophisticated approach
        # For now, just set the first artist
        if artists:
            command = ["bwfmetaedit", f"--IART={artists[0]}", str(file_path)]
            BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_multiple_genres(file_path: Path, genres: List[str]):
        """Set RIFF multiple genres using external tool."""
        # For now, just set the first genre
        if genres:
            command = ["bwfmetaedit", f"--IGNR={genres[0]}", str(file_path)]
            BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_multiple_composers(file_path: Path, composers: List[str]):
        """Set RIFF multiple composers using external tool."""
        # For now, just set the first composer
        if composers:
            command = ["bwfmetaedit", f"--ICMP={composers[0]}", str(file_path)]
            BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_multiple_album_artists(file_path: Path, album_artists: List[str]):
        """Set RIFF multiple album artists using external tool."""
        # For now, just set the first album artist
        if album_artists:
            command = ["bwfmetaedit", f"--IAAR={album_artists[0]}", str(file_path)]
            BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_multiple_comments(file_path: Path, comments: List[str]):
        """Set RIFF multiple comments using external tool."""
        # For now, just set the first comment
        if comments:
            command = ["bwfmetaedit", f"--ICMT={comments[0]}", str(file_path)]
            BwfmetaeditTool.run_command(command)