"""ID3v2 separator-based metadata manager for testing single-field separator parsing."""

from pathlib import Path

from .mid3v2_tool import Mid3v2Tool


class ID3v2SeparatorMetadataManager:
    """Manager for setting ID3v2 metadata using separator-based approaches for testing single-field separator parsing."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
    
    def set_separator_artists(self, artists_string: str, version: str = "2.3"):
        """Set ID3v2 artists as a single field with separators using external tool."""
        command = ["mid3v2", "--artist", artists_string, str(self.file_path)]
        Mid3v2Tool.run_command(command)
    
    def set_separator_genres(self, genres_string: str, version: str = "2.3"):
        """Set ID3v2 genres as a single field with separators using external tool."""
        command = ["mid3v2", "--genre", genres_string, str(self.file_path)]
        Mid3v2Tool.run_command(command)
    
    def set_separator_composers(self, composers_string: str, version: str = "2.3"):
        """Set ID3v2 composers as a single field with separators using external tool."""
        command = ["mid3v2", "--TCOM", composers_string, str(self.file_path)]
        Mid3v2Tool.run_command(command)