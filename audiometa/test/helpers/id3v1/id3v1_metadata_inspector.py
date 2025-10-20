"""ID3v1 metadata inspection utilities for testing audio file metadata."""

from pathlib import Path
from typing import Dict, Any


class ID3v1MetadataInspector:
    """Utilities for inspecting ID3v1 metadata in audio files."""
    
    @staticmethod
    def inspect_raw_field(file_path: Path, field_name: str) -> Dict[str, Any]:
        """Inspect a specific field in raw ID3v1 data.
        
        Args:
            file_path: Path to the audio file
            field_name: The field to inspect ('title', 'artist', 'album', 'year', 'comment', 'genre', 'track')
        
        Returns:
            Dictionary with inspection results including:
            - success: Whether the inspection succeeded
            - field_value: The raw field value as stored in ID3v1
            - has_data: Whether the field contains data
            - is_truncated: Whether the field appears to be truncated (for string fields)
        """
        try:
            with open(file_path, 'rb') as f:
                f.seek(-128, 2)  # Seek to last 128 bytes (ID3v1 tag location)
                data = f.read(128)
            
            # Check for ID3v1 tag header
            if not data.startswith(b'TAG'):
                return {
                    'success': False,
                    'error': 'No ID3v1 tag found',
                    'field_value': None,
                    'has_data': False,
                    'is_truncated': False
                }
            
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
            
            if field_name not in field_info:
                return {
                    'success': False,
                    'error': f'Unknown field: {field_name}',
                    'field_value': None,
                    'has_data': False,
                    'is_truncated': False
                }
            
            start, end, max_len = field_info[field_name]
            
            if field_name == 'genre':
                # Genre is stored as a single byte (0-255)
                field_value = data[start]
                has_data = field_value != 255  # 255 = undefined genre
                is_truncated = False
            elif field_name == 'track':
                # Track number in ID3v1.1 (byte 125, if byte 124 is 0)
                if len(data) >= 126 and data[124] == 0 and data[125] != 0:
                    field_value = data[start]
                    has_data = field_value != 0
                else:
                    field_value = None
                    has_data = False
                is_truncated = False
            else:
                # String fields
                raw_bytes = data[start:end]
                field_value = raw_bytes.strip(b'\0').decode('latin1', 'replace')
                has_data = bool(field_value.strip())
                # Check if truncated (field is exactly max length and doesn't end with null byte)
                is_truncated = len(raw_bytes.rstrip(b'\0')) == max_len
            
            return {
                'success': True,
                'field_value': field_value,
                'has_data': has_data,
                'is_truncated': is_truncated,
                'max_length': max_len,
                'field_name': field_name
            }
            
        except (IOError, OSError) as e:
            return {
                'success': False,
                'error': str(e),
                'field_value': None,
                'has_data': False,
                'is_truncated': False
            }
    
    @staticmethod
    def inspect_artist_field(file_path: Path) -> Dict[str, Any]:
        """Inspect the artist field specifically, with additional checks for multiple artists.
        
        For ID3v1, multiple artists are concatenated into a single 30-character field,
        typically separated by commas, semicolons, or other delimiters.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with inspection results including:
            - success: Whether the inspection succeeded  
            - artist_value: The raw artist string as stored in ID3v1
            - has_data: Whether the artist field contains data
            - is_truncated: Whether the artist field appears to be truncated
            - contains_separators: Whether the field contains common separators
            - detected_separators: List of separators found in the field
        """
        result = ID3v1MetadataInspector.inspect_raw_field(file_path, 'artist')
        
        if not result['success'] or not result['has_data']:
            result.update({
                'artist_value': result.get('field_value'),
                'contains_separators': False,
                'detected_separators': []
            })
            return result
        
        artist_value = result['field_value']
        
        # Check for common separators used for multiple artists
        common_separators = [', ', ',', '; ', ';', ' / ', '/', ' & ', '&', ' and ', ' + ', '+']
        detected_separators = []
        
        for sep in common_separators:
            if sep in artist_value:
                detected_separators.append(sep)
        
        result.update({
            'artist_value': artist_value,
            'contains_separators': len(detected_separators) > 0,
            'detected_separators': detected_separators
        })
        
        return result