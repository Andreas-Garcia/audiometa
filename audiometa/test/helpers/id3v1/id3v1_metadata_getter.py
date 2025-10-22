"""ID3v1 metadata inspection utilities for testing audio file metadata."""

from pathlib import Path
from typing import Dict, Any


class ID3v1MetadataGetter:
    """Utilities for inspecting ID3v1 metadata in audio files."""
    
    @staticmethod
    def get_raw_metadata(file_path: Path) -> Dict[str, Any]:
        """Return the raw metadata for a specific ID3v1 field."""
        with open(file_path, 'rb') as f:
            f.seek(-128, 2)  # Seek to last 128 bytes (ID3v1 tag location)
            data = f.read(128)
        
        # Check for ID3v1 tag header
        if not data.startswith(b'TAG'):
            return {}
        
        # Parse fields based on ID3v1 specification
        field_info = {
            'title': (3, 33, 30),      # bytes 3-32, 30 chars max
            'artist': (33, 63, 30),    # bytes 33-62, 30 chars max  
            'album': (63, 93, 30),     # bytes 63-92, 30 chars max
            'year': (93, 97, 4),       # bytes 93-96, 4 chars max
            'comment': (97, 125, 28),  # bytes 97-124, 28 chars max (ID3v1.1)
            'track': (125, 126, 1),    # byte 125 (ID3v1.1)
            'genre': (127, 128, 1)     # byte 127
        }
        
        metadata = {}
        for field, (start, end, max_chars) in field_info.items():
            raw_bytes = data[start:end]
            if field in ['title', 'artist', 'album', 'year', 'comment']:
                metadata[field] = raw_bytes.decode('latin-1').rstrip('\x00')
            elif field == 'track':
                metadata[field] = raw_bytes[0] if raw_bytes and raw_bytes[0] != 0 else None
            elif field == 'genre':
                metadata[field] = raw_bytes[0] if raw_bytes else 0
        
        return metadata

    @staticmethod
    def get_title(file_path):
        metadata = ID3v1MetadataGetter.get_raw_metadata(file_path)
        return metadata.get('title', '')