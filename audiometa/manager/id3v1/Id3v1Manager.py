
from typing import cast
from mutagen._file import FileType as MutagenMetadata

from ...audio_file import AudioFile
from ...exceptions import FileCorruptedError, MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ...utils.types import AppMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import MetadataManager
from .Id3v1RawMetadata import Id3v1RawMetadata
from .Id3v1RawMetadataKey import Id3v1RawMetadataKey


class Id3v1Manager(MetadataManager):
    """
    Manages ID3v1 metadata for audio files.

    ID3v1 is a simple, legacy metadata format with significant limitations:
    - Fixed 128-byte block at end of file
    - No Unicode support (Latin-1 only)
    - Limited field lengths (30 chars)
    - No support for:
        - Album artist
        - BPM
        - Ratings
        - Language
        - Custom genres
        - Multiple genres
        - Multiple artists
        ...
    - Supports both reading and writing metadata using direct file manipulation.

    Format Structure:
    - Bytes 0-2: "TAG" identifier
    - Bytes 3-32: Title (30 chars)
    - Bytes 33-62: Artist (30 chars)
    - Bytes 63-92: Album (30 chars)
    - Bytes 93-96: Release year (4 chars)
    - Bytes 97-126: Comment (28 chars in ID3v1.1, 30 chars in ID3v1)
    - Byte 125: Always 0 in ID3v1.1 to indicate track number presence
    - Byte 126: Track number in ID3v1.1 (1-255, 0 = not set)
    - Byte 127: Genre code (0-255)

    Note: ID3v1.1 extends ID3v1 by using the last two bytes of the comment
    field to store the track number. If byte 125 is 0 and byte 126 is not 0,
    then byte 126 contains the track number (1-255).

    Note 2: The genre code is an index into a predefined list of genres.

    Supported File Formats:
    - MP3: Native ID3v1 format, optimal support
    - FLAC: Some FLAC files may contain ID3v1 tags (not optimal but supported)
    - WAV: Some WAV files may contain ID3v1 tags (not optimal but supported)
    
    While ID3v1 is natively designed for MP3 files, this manager supports reading
    ID3v1 tags from FLAC and WAV files when present, even though it's not the
    optimal metadata format for these file types.
    """

    def __init__(self, audio_file: AudioFile):
        metadata_keys_direct_map_read: dict = {
            UnifiedMetadataKey.TITLE: Id3v1RawMetadataKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: Id3v1RawMetadataKey.ARTISTS_NAMES_STR,
            UnifiedMetadataKey.ALBUM_NAME: Id3v1RawMetadataKey.ALBUM_NAME,
            UnifiedMetadataKey.GENRE_NAME: None,
        }
        metadata_keys_direct_map_write: dict = {
            UnifiedMetadataKey.TITLE: Id3v1RawMetadataKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: Id3v1RawMetadataKey.ARTISTS_NAMES_STR,
            UnifiedMetadataKey.ALBUM_NAME: Id3v1RawMetadataKey.ALBUM_NAME,
            UnifiedMetadataKey.RELEASE_DATE: Id3v1RawMetadataKey.YEAR,
            UnifiedMetadataKey.TRACK_NUMBER: Id3v1RawMetadataKey.TRACK_NUMBER,
            UnifiedMetadataKey.COMMENT: Id3v1RawMetadataKey.COMMENT,
            UnifiedMetadataKey.GENRE_NAME: None,  # Handled indirectly
        }
        super().__init__(
            audio_file=audio_file, 
            metadata_keys_direct_map_read=metadata_keys_direct_map_read,
            metadata_keys_direct_map_write=metadata_keys_direct_map_write,
            update_using_mutagen_metadata=False  # Use direct file manipulation for ID3v1
        )

    def _extract_mutagen_metadata(self) -> Id3v1RawMetadata:
        try:
            return Id3v1RawMetadata(fileobj=self.audio_file.get_file_path_or_object())
        except Exception as exc:
            raise FileCorruptedError(f"Failed to extract ID3v1 metadata: {exc}")

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        raw_metadata_id3v1: Id3v1RawMetadata = cast(Id3v1RawMetadata, raw_mutagen_metadata)
        if not raw_metadata_id3v1.tags:
            return {}

        # Create a mapping of string values to enum members with proper value types
        result: RawMetadataDict = {}
        for key, value in raw_metadata_id3v1.tags.items():
            # Skip empty values
            if not value:
                continue

            # Find the matching enum member by its value
            for enum_member in Id3v1RawMetadataKey:
                if enum_member == key:
                    result[enum_member] = value
        return result

    def _get_undirectly_mapped_metadata_value_from_raw_clean_metadata(
            self, raw_clean_metadata: RawMetadataDict, app_metadata_key: UnifiedMetadataKey) -> AppMetadataValue:
        if app_metadata_key == UnifiedMetadataKey.GENRE_NAME:
            return self._get_genre_name_from_raw_clean_metadata_id3v1(
                raw_clean_metadata=raw_clean_metadata, raw_metadata_ket=Id3v1RawMetadataKey.GENRE_CODE_OR_NAME)
        raise MetadataNotSupportedError(f'{app_metadata_key} metadata is not undirectly handled')

    def _update_undirectly_mapped_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                           app_metadata_value: AppMetadataValue,
                                           app_metadata_key: UnifiedMetadataKey):
        if app_metadata_key == UnifiedMetadataKey.GENRE_NAME:
            # Convert genre name to genre code
            genre_code = self._convert_genre_name_to_code(app_metadata_value)
            if genre_code is not None:
                raw_mutagen_metadata.tags[Id3v1RawMetadataKey.GENRE_CODE_OR_NAME] = [str(genre_code)]
        else:
            raise MetadataNotSupportedError(f'{app_metadata_key} metadata is not undirectly handled')

    def _update_formatted_value_in_raw_mutagen_metadata(self, raw_mutagen_metadata: MutagenMetadata,
                                                        raw_metadata_key: RawMetadataKey,
                                                        app_metadata_value: AppMetadataValue):
        # Ensure tags exist
        if not hasattr(raw_mutagen_metadata, 'tags') or raw_mutagen_metadata.tags is None:
            raw_mutagen_metadata.tags = {}
        
        # Convert and truncate the value according to ID3v1 constraints
        if raw_metadata_key == Id3v1RawMetadataKey.TITLE:
            value = self._truncate_string(str(app_metadata_value), 30)
        elif raw_metadata_key == Id3v1RawMetadataKey.ARTISTS_NAMES_STR:
            # Convert list to string and truncate
            artists_str = ", ".join(app_metadata_value) if isinstance(app_metadata_value, list) else str(app_metadata_value)
            value = self._truncate_string(artists_str, 30)
        elif raw_metadata_key == Id3v1RawMetadataKey.ALBUM_NAME:
            value = self._truncate_string(str(app_metadata_value), 30)
        elif raw_metadata_key == Id3v1RawMetadataKey.YEAR:
            value = self._truncate_string(str(app_metadata_value), 4)
        elif raw_metadata_key == Id3v1RawMetadataKey.TRACK_NUMBER:
            # Convert to int and validate range
            track_num = int(app_metadata_value) if app_metadata_value is not None else 0
            value = str(max(0, min(255, track_num)))
        elif raw_metadata_key == Id3v1RawMetadataKey.COMMENT:
            value = self._truncate_string(str(app_metadata_value), 28)  # 28 for ID3v1.1 with track number
        else:
            value = str(app_metadata_value)
        
        raw_mutagen_metadata.tags[raw_metadata_key] = [value]

    def _update_not_using_mutagen_metadata(self, app_metadata: AppMetadata):
        """Update ID3v1 metadata using direct file manipulation."""
        # Read the entire file
        self.audio_file.seek(0)
        file_data = bytearray(self.audio_file.read())
        
        # Create ID3v1 tag data
        tag_data = self._create_id3v1_tag_data(app_metadata)
        
        # Find and remove existing ID3v1 tag if present
        self._remove_existing_id3v1_tag(file_data)
        
        # Append new ID3v1 tag
        file_data.extend(tag_data)
        
        # Write back to file
        self.audio_file.write(file_data)

    def _create_id3v1_tag_data(self, app_metadata: AppMetadata) -> bytes:
        """Create 128-byte ID3v1 tag data from app metadata."""
        # Initialize with null bytes
        tag_data = bytearray(128)
        
        # TAG identifier (bytes 0-2)
        tag_data[0:3] = b'TAG'
        
        # Title (bytes 3-32, 30 chars max)
        title = str(app_metadata.get(UnifiedMetadataKey.TITLE, ''))
        title_bytes = self._truncate_string(title, 30).encode('latin-1', errors='ignore')
        tag_data[3:3+len(title_bytes)] = title_bytes
        
        # Artist (bytes 33-62, 30 chars max)
        artists = app_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES, [])
        artist_str = ", ".join(artists) if isinstance(artists, list) else str(artists)
        artist_bytes = self._truncate_string(artist_str, 30).encode('latin-1', errors='ignore')
        tag_data[33:33+len(artist_bytes)] = artist_bytes
        
        # Album (bytes 63-92, 30 chars max)
        album = str(app_metadata.get(UnifiedMetadataKey.ALBUM_NAME, ''))
        album_bytes = self._truncate_string(album, 30).encode('latin-1', errors='ignore')
        tag_data[63:63+len(album_bytes)] = album_bytes
        
        # Year (bytes 93-96, 4 chars max)
        year = str(app_metadata.get(UnifiedMetadataKey.RELEASE_DATE, ''))
        year_bytes = self._truncate_string(year, 4).encode('latin-1', errors='ignore')
        tag_data[93:93+len(year_bytes)] = year_bytes
        
        # Comment and track number (bytes 97-126, 28 chars for comment + 2 for track)
        comment = str(app_metadata.get(UnifiedMetadataKey.COMMENT, ''))
        comment_bytes = self._truncate_string(comment, 28).encode('latin-1', errors='ignore')
        tag_data[97:97+len(comment_bytes)] = comment_bytes
        
        # Track number (bytes 125-126 for ID3v1.1)
        track_number = app_metadata.get(UnifiedMetadataKey.TRACK_NUMBER)
        if track_number is not None:
            track_num = max(0, min(255, int(track_number)))
            if track_num > 0:
                tag_data[125] = 0  # Null byte to indicate track number presence
                tag_data[126] = track_num
        
        # Genre (byte 127)
        genre_name = app_metadata.get(UnifiedMetadataKey.GENRE_NAME)
        if genre_name:
            genre_code = self._convert_genre_name_to_code(genre_name)
            if genre_code is not None:
                tag_data[127] = genre_code
            else:
                tag_data[127] = 255  # Unknown genre
        
        return bytes(tag_data)

    def _remove_existing_id3v1_tag(self, file_data: bytearray) -> bool:
        """Remove existing ID3v1 tag from file data if present.
        
        Returns:
            bool: True if a tag was removed, False otherwise
        """
        if len(file_data) >= 128:
            # Check if last 128 bytes contain ID3v1 tag
            last_128 = file_data[-128:]
            if last_128[:3] == b'TAG':
                # Remove the last 128 bytes
                del file_data[-128:]
                return True
        return False

    def _truncate_string(self, text: str, max_length: int) -> str:
        """Truncate string to maximum length, handling encoding properly."""
        if len(text) <= max_length:
            return text
        return text[:max_length]

    def _convert_genre_name_to_code(self, genre_name: str) -> int | None:
        """Convert genre name to ID3v1 genre code."""
        from ..MetadataManager import ID3V1_GENRE_CODE_MAP
        
        # First try exact match
        for code, name in ID3V1_GENRE_CODE_MAP.items():
            if name and name.lower() == genre_name.lower():
                return code
        
        # Try partial match
        for code, name in ID3V1_GENRE_CODE_MAP.items():
            if name and genre_name.lower() in name.lower():
                return code
        
        return None

    def delete_metadata(self) -> bool:
        """Delete ID3v1 metadata from the audio file.
        
        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Read the entire file
            self.audio_file.seek(0)
            file_data = bytearray(self.audio_file.read())
            
            # Remove existing ID3v1 tag if present
            if self._remove_existing_id3v1_tag(file_data):
                # Write back to file
                self.audio_file.write(file_data)
                return True
            return False
        except Exception:
            return False

    def get_header_info(self) -> dict:
        try:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = self._extract_mutagen_metadata()
            
            if not self.raw_mutagen_metadata:
                return {
                    'present': False,
                    'position': 'end_of_file',
                    'size_bytes': 0,
                    'version': None,
                    'has_track_number': False
                }
            
            # Check if ID3v1 tag is present
            present = hasattr(self.raw_mutagen_metadata, 'tags') and self.raw_mutagen_metadata.tags is not None
            
            if not present:
                return {
                    'present': False,
                    'position': 'end_of_file',
                    'size_bytes': 0,
                    'version': None,
                    'has_track_number': False
                }
            
            # Determine version (ID3v1 or ID3v1.1)
            version = '1.0'
            has_track_number = False
            
            if hasattr(self.raw_mutagen_metadata, 'tags'):
                # Check if track number is present (ID3v1.1 feature)
                comment = self.raw_mutagen_metadata.tags.get('COMMENT', [''])[0]
                if len(comment) >= 2 and comment[-2] == '\x00' and comment[-1] != '\x00':
                    version = '1.1'
                    has_track_number = True
            
            return {
                'present': True,
                'position': 'end_of_file',
                'size_bytes': 128,
                'version': version,
                'has_track_number': has_track_number
            }
        except Exception:
            return {
                'present': False,
                'position': 'end_of_file',
                'size_bytes': 0,
                'version': None,
                'has_track_number': False
            }

    def get_raw_metadata_info(self) -> dict:
        """Get raw ID3v1 metadata information."""
        try:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = self._extract_mutagen_metadata()
            
            if not self.raw_mutagen_metadata or not hasattr(self.raw_mutagen_metadata, 'tags'):
                return {
                    'raw_data': None,
                    'parsed_fields': {},
                    'frames': {},
                    'comments': {},
                    'chunk_structure': {}
                }
            
            # Get parsed fields
            parsed_fields = {}
            if self.raw_mutagen_metadata.tags:
                for key, value in self.raw_mutagen_metadata.tags.items():
                    parsed_fields[key] = value[0] if value else ''
            
            return {
                'raw_data': None,  # ID3v1 is 128 bytes at end of file
                'parsed_fields': parsed_fields,
                'frames': {},
                'comments': {},
                'chunk_structure': {}
            }
        except Exception:
            return {
                'raw_data': None,
                'parsed_fields': {},
                'frames': {},
                'comments': {},
                'chunk_structure': {}
            }
