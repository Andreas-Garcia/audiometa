
from typing import cast
from mutagen._file import FileType as MutagenMetadata

from ...audio_file import AudioFile
from ...exceptions import FileCorruptedError, MetadataNotSupportedError
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from ...utils.types import AppMetadataValue, RawMetadataDict
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
    - Read-only (modification not supported). ID3v1 tags have a fixed size of 128 bytes. Each field within the tag has a 
    specific length (e.g., 30 bytes for title, artist, and album). This fixed size makes it challenging to modify the 
    tags without potentially corrupting the file or losing data. Therefore, this manager only supports reading metadata.

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
        super().__init__(audio_file=audio_file, metadata_keys_direct_map_read=metadata_keys_direct_map_read,)

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

    def _update_undirectly_mapped_metadata(self, app_metadata_value: AppMetadataValue,
                                           app_metadata_key: UnifiedMetadataKey,
                                           normalized_rating_max_value: int | None = None):
        raise MetadataNotSupportedError("ID3v1 tag modification is not supported")

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
