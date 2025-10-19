"""RIFF separator-based metadata manager for testing single-field separator parsing."""

from pathlib import Path

from .bwfmetaedit_tool import BwfmetaeditTool


class RIFFSeparatorMetadataManager:
    """Static utility class for setting RIFF metadata using separator-based approaches for testing single-field separator parsing."""
    
    @staticmethod
    def set_separator_artists(file_path: Path, artists_string: str):
        """Set RIFF artists as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--IART={artists_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_genres(file_path: Path, genres_string: str):
        """Set RIFF genres as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--IGNR={genres_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_composers(file_path: Path, composers_string: str):
        """Set RIFF composers as a single field with separators using external tool."""
        command = ["bwfmetaedit", f"--ICMP={composers_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)
    
    @staticmethod
    def set_separator_album_artists(file_path: Path, album_artists_string: str):
        """Set RIFF album artists as a single field with separators using external tool."""
        # RIFF doesn't have a standard album artist field, using a custom approach
        command = ["bwfmetaedit", f"--IAAR={album_artists_string}", str(file_path)]
        BwfmetaeditTool.run_command(command)