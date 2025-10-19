"""RIFF separator-based metadata manager for testing single-field separator parsing."""

from pathlib import Path

from .bwfmetaedit_tool import BwfmetaeditTool


class RIFFSeparatorMetadataManager:
    """Manager for setting RIFF metadata using separator-based approaches for testing single-field separator parsing."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def set_separator_artists(self, artists_string: str):
        """Set RIFF artists as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--IART={artists_string}", str(self.file_path)]
        BwfmetaeditTool.run_command(command)
    
    def set_separator_genres(self, genres_string: str):
        """Set RIFF genres as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--IGNR={genres_string}", str(self.file_path)]
        BwfmetaeditTool.run_command(command)
    
    def set_separator_composers(self, composers_string: str):
        """Set RIFF composers as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--ICMP={composers_string}", str(self.file_path)]
        BwfmetaeditTool.run_command(command)
    
    def set_separator_album_artists(self, album_artists_string: str):
        """Set RIFF album artists as a single field with separators using external tool."""
        # RIFF doesn't have a standard album artist field, using a custom approach
        command = ["bwfmetaedit", f"--IAAR={album_artists_string}", str(self.file_path)]
        BwfmetaeditTool.run_command(command)