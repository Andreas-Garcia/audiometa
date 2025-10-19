"""Separator-based metadata manager facade for testing single-field separator parsing across formats."""

from pathlib import Path
from typing import Dict, Any

from ..id3v2 import ID3v2SeparatorMetadataManager
from ..riff import RIFFMetadataSetter


class SeparatorBasedMetadataManager:
    """Facade manager providing format-agnostic separator-based metadata operations.
    
    This class provides a unified interface for setting separator-based metadata
    across different audio formats without exposing format-specific details.
    """
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.id3v2_manager = ID3v2SeparatorMetadataManager(file_path)
    
    def set_separator_metadata(self, metadata_format: str, field: str, value: str, **kwargs):
        """Set separator-based metadata for any format and field.
        
        Args:
            metadata_format: The format ('id3v2', 'riff')
            field: The metadata field ('artists', 'genres', 'composers', 'album_artists')
            value: The separator-delimited string value
            **kwargs: Additional format-specific options (e.g., version for ID3v2)
        """
        if metadata_format.lower() == 'id3v2':
            manager = self.id3v2_manager
            version = kwargs.get('version', '2.3')
            if field == 'artists':
                manager.set_separator_artists(value, version)
            elif field == 'genres':
                manager.set_separator_genres(value, version)
            elif field == 'composers':
                manager.set_separator_composers(value, version)
            else:
                raise ValueError(f"Unsupported ID3v2 field: {field}")
                
        elif metadata_format.lower() == 'riff':
            if field == 'artists':
                RIFFMetadataSetter.set_separator_artists(self.file_path, value)
            elif field == 'genres':
                RIFFMetadataSetter.set_separator_genres(self.file_path, value)
            elif field == 'composers':
                RIFFMetadataSetter.set_separator_composers(self.file_path, value)
            elif field == 'album_artists':
                RIFFMetadataSetter.set_separator_album_artists(self.file_path, value)
            else:
                raise ValueError(f"Unsupported RIFF field: {field}")
        else:
            raise ValueError(f"Unsupported metadata format: {metadata_format}")
    
    def get_supported_formats(self) -> Dict[str, list]:
        """Get supported formats and their supported fields."""
        return {
            'id3v2': ['artists', 'genres', 'composers'],
            'riff': ['artists', 'genres', 'composers', 'album_artists']
        }