"""RIFF multiple metadata manager for creating test files with specific configurations."""

from pathlib import Path
from typing import List

from .bwfmetaedit_tool import BwfmetaeditTool


class RIFFMultipleMetadataManager:
    """Manager for setting multiple values in RIFF metadata."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def set_multiple_artists(self, artists: List[str]):
        """Set RIFF multiple artists using external tool (creates multiple chunks)."""
        # For testing multiple instances, we'd need to use a more sophisticated approach
        # For now, just set the first artist
        if artists:
            command = ["bwfmetaedit", f"--IART={artists[0]}", str(self.file_path)]
            BwfmetaeditTool.run_command(command)
    
    def set_multiple_genres(self, genres: List[str]):
        """Set RIFF multiple genres using external tool."""
        # For now, just set the first genre
        if genres:
            command = ["bwfmetaedit", f"--IGNR={genres[0]}", str(self.file_path)]
            BwfmetaeditTool.run_command(command)
    
    def set_multiple_composers(self, composers: List[str]):
        """Set RIFF multiple composers using external tool."""
        # For now, just set the first composer
        if composers:
            command = ["bwfmetaedit", f"--ICMP={composers[0]}", str(self.file_path)]
            BwfmetaeditTool.run_command(command)
    
    def set_multiple_album_artists(self, album_artists: List[str]):
        """Set RIFF multiple album artists using external tool."""
        # For now, just set the first album artist
        if album_artists:
            command = ["bwfmetaedit", f"--IAAR={album_artists[0]}", str(self.file_path)]
            BwfmetaeditTool.run_command(command)
    
    def set_multiple_comments(self, comments: List[str]):
        """Set RIFF multiple comments using external tool."""
        # For now, just set the first comment
        if comments:
            command = ["bwfmetaedit", f"--ICMT={comments[0]}", str(self.file_path)]
            BwfmetaeditTool.run_command(command)