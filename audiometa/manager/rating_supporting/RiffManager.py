import contextlib
import os
from typing import cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.wave import WAVE

from ...audio_file import AudioFile
from ...exceptions import ConfigurationError, MetadataNotSupportedError, FileTypeNotSupportedError
from ...utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP
from ...utils.rating_profiles import RatingWriteProfile
from ...utils.types import AppMetadata, AppMetadataValue, RawMetadataDict, RawMetadataKey
from ..MetadataManager import UnifiedMetadataKey
from ..rating_supporting.RatingSupportingMetadataManager import RatingSupportingMetadataManager


class RiffManager(RatingSupportingMetadataManager):
    """
    Manages RIFF metadata for WAV audio files.

    Implementation Note:
    While mutagen is used for reading WAV metadata, it does not support writing RIFF metadata. This is a known
    limitation of the library, which only provides read-only access to WAVE files' metadata through its WAVE class.
    Therefore, this manager implements its own RIFF metadata writing functionality by directly manipulating the file's
    INFO chunk according to the RIFF specification.

    RIFF Format:
    RIFF (Resource Interchange File Format) is the standard metadata format for WAV files. The INFO chunk in RIFF/WAV
    files uses standardized 4-character codes (FourCC) like INAM(Title), IART(Artist) or ICMT(Comments).

    These codes are defined in RiffTagKey and are part of the standard RIFF specification. Each tag in the INFO chunk
    follows the format:
    - FourCC (4 chars): Identifies the metadata field (e.g., 'INAM' for title)
    - Size (4 bytes): Length of the data in bytes
    - Data (UTF-8): The actual metadata content
    - Padding: If needed for word alignment (2 bytes)

    Genre Support:
    The IGNR tag in RIFF files has two modes:
    1. Genre Code (Preferred): Uses the standard ID3v1/RIFF genre list (0-147)
       - Limited to predefined genres
       - Compatible with older software
       - No custom genres
       - No multiple genres
    2. Text Mode (Less Common): Direct genre name as text
       - Less widely supported
       - May not work with all software
       - Use genre codes for better compatibility

    Unsupported Metadata:
    RIFF format has limited metadata support compared to other formats. The following metadata fields are NOT supported
    and will raise MetadataNotSupportedError if provided:
    - Rating: RIFF format does not have a standard rating field
    - Genre: Limited to predefined genre codes (0-147) or text mode
    
    When attempting to update unsupported metadata, the manager will raise MetadataNotSupportedError with a clear
    message indicating which field is not supported by the RIFF format.

    Note: This manager is the preferred way to handle WAV metadata, as it uses the format's native metadata system
    rather than non-standard alternatives like ID3v2 tags. The custom implementation ensures proper handling of RIFF
    chunk structures, maintaining word alignment and size fields according to the specification.
    """

    class RiffTagKey(RawMetadataKey):
        # Standard
        TITLE = 'INAM'
        ARTIST_NAME = 'IART'
        ALBUM_NAME = 'IPRD'
        GENRE_NAME_OR_CODE = 'IGNR'
        DATE = 'ICRD'  # Creation/Release date
        TRACK_NUMBER = 'IPRT'

        # Non-standard
        ALBUM_ARTISTS_NAMES = 'IAAR'
        LANGUAGE = 'ILNG'
        RATING = 'IRTD'
        COMMENTS = 'ICMT'
        ENGINEER = 'IENG'  # Engineer who worked on the track
        SOFTWARE = 'ISFT'  # Software used to create the file
        COPYRIGHT = 'ICOP'
        TECHNICIAN = 'ITCH'  # Technician who worked on the track

    def __init__(self, audio_file: AudioFile, normalized_rating_max_value: None | int = None):
        # Validate that the file is a WAV file
        if audio_file.file_extension != '.wav':
            raise FileTypeNotSupportedError(f"RiffManager only supports WAV files, got {audio_file.file_extension}")
        
        metadata_keys_direct_map_read = {
            UnifiedMetadataKey.TITLE: self.RiffTagKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: self.RiffTagKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            UnifiedMetadataKey.GENRE_NAME: None,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: None,
        }
        metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None] = {
            UnifiedMetadataKey.TITLE: self.RiffTagKey.TITLE,
            UnifiedMetadataKey.ARTISTS_NAMES: self.RiffTagKey.ARTIST_NAME,
            UnifiedMetadataKey.ALBUM_NAME: self.RiffTagKey.ALBUM_NAME,
            UnifiedMetadataKey.ALBUM_ARTISTS_NAMES: self.RiffTagKey.ALBUM_ARTISTS_NAMES,
            UnifiedMetadataKey.GENRE_NAME: None,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            # AppMetadataKey.TRACK_NUMBER: self.RiffTagKey.TRACK_NUMBER,
        }
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write,
                         rating_write_profile=RatingWriteProfile.BASE_100_PROPORTIONAL,
                         normalized_rating_max_value=normalized_rating_max_value,
                         update_using_mutagen_metadata=False)

    def _skip_id3v2_tags(self, data: bytes) -> bytes:
        """
        Skip ID3v2 tags if present at the start of the file.
        Returns the data starting from after any ID3v2 tags.
        """
        if data.startswith(b'ID3'):
            # ID3v2 header is 10 bytes:
            # 3 bytes: ID3
            # 2 bytes: version
            # 1 byte: flags
            # 4 bytes: size (synchsafe integer)
            if len(data) < 10:
                return data

            # Get size from synchsafe integer (7 bits per byte)
            size_bytes = data[6:10]
            size = ((size_bytes[0] & 0x7F) << 21) | \
                   ((size_bytes[1] & 0x7F) << 14) | \
                   ((size_bytes[2] & 0x7F) << 7) | \
                   (size_bytes[3] & 0x7F)

            # Skip the header (10 bytes) plus the size of the tag
            return data[10 + size:]
        return data

    def _extract_riff_metadata_directly(self, file_data: bytes) -> dict[str, str]:
        """
        Manually extract metadata from RIFF chunks without relying on external libraries.
        This method directly parses the RIFF structure to extract metadata from the INFO chunk.
        """
        info_tags: dict[str, str] = {}

        # Skip ID3v2 if present
        file_data = self._skip_id3v2_tags(file_data)

        # Validate RIFF header
        if len(file_data) < 12 or file_data[:4] != b'RIFF' or file_data[8:12] != b'WAVE':
            return info_tags

        pos = 12  # Start after RIFF header
        while pos < len(file_data) - 8:
            chunk_id = file_data[pos:pos + 4]
            chunk_size = int.from_bytes(file_data[pos + 4:pos + 8], 'little')

            if chunk_id == b'LIST' and pos + 12 <= len(file_data):
                if file_data[pos + 8:pos + 12] == b'INFO':
                    # Process INFO chunk
                    info_pos = pos + 12
                    info_end = pos + 8 + chunk_size

                    while info_pos < info_end - 8:
                        # Extract each metadata field
                        field_id = file_data[info_pos:info_pos + 4].decode('ascii', errors='ignore')
                        field_size = int.from_bytes(file_data[info_pos + 4:info_pos + 8], 'little')

                        if field_size > 0 and info_pos + 8 + field_size <= info_end:
                            # -1 to exclude null terminator
                            field_data = file_data[info_pos + 8:info_pos + 8 + field_size - 1]
                            try:
                                # Decode and handle null-terminated strings
                                field_value = field_data.decode('utf-8', errors='ignore')
                                # Split on null byte and take first part if exists
                                field_value = field_value.split('\x00')[0].strip()
                                if field_id in self.RiffTagKey and field_value:
                                    info_tags[field_id] = field_value
                            except UnicodeDecodeError:
                                pass

                        # Move to next field, maintaining alignment
                        info_pos += 8 + ((field_size + 1) & ~1)
                    break

            # Move to next chunk, maintaining alignment
            pos += 8 + ((chunk_size + 1) & ~1)

        return info_tags

    @contextlib.contextmanager
    def _suppress_output(self):
        """Context manager to suppress all output including direct prints."""
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                yield

    def _extract_mutagen_metadata(self) -> MutagenMetadata:
        """
        Extract RIFF metadata from WAV files using direct RIFF chunk parsing.
        This method reads the WAV file's INFO chunk directly, providing the most
        reliable way to access RIFF metadata.
        """
        self.audio_file.seek(0)
        file_data = self.audio_file.read()

        # Skip ID3v2 metadata if present and create a clean RIFF file for mutagen
        clean_data = self._skip_id3v2_tags(file_data)
        
        # Create a temporary file with just the RIFF data for mutagen to parse
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(clean_data)
            temp_file.flush()
            
            try:
                # Create WAVE object with the clean RIFF data
                wave = WAVE(filename=temp_file.name)
                info_tags = self._extract_riff_metadata_directly(file_data)  # Use original data for our custom parsing
                setattr(wave, 'info', info_tags)
                return wave
            finally:
                # Clean up temporary file
                import os
                try:
                    os.unlink(temp_file.name)
                except OSError:
                    pass

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
            self, raw_mutagen_metadata: MutagenMetadata) -> RawMetadataDict:
        """
        Convert RIFF metadata to dictionary.
        Extracts tags from our custom info_tags attribute which contains
        the directly parsed INFO chunk data.
        """
        raw_mutagen_metadata_wav: WAVE = cast(WAVE, raw_mutagen_metadata)
        raw_metadata_dict: dict = {}

        # Get metadata from our custom info which contains the directly parsed INFO chunk
        if hasattr(raw_mutagen_metadata_wav, 'info'):
            info_tags = getattr(raw_mutagen_metadata_wav, 'info')
            for key, value in info_tags.items():
                if key in self.RiffTagKey:
                    raw_metadata_dict[key] = value

        return raw_metadata_dict

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        if not self.RiffTagKey.RATING in raw_clean_metadata:
            return None, False

        raw_ratings = raw_clean_metadata.get(self.RiffTagKey.RATING)
        if not raw_ratings or len(raw_ratings) == 0:
            return None, False

        raw_rating = raw_ratings[0]
        if not raw_rating:
            return None, False

        if isinstance(raw_rating, str):
            return int(raw_rating), False
        return cast(int, raw_rating), True

    def _get_undirectly_mapped_metadata_value_other_than_rating_from_raw_clean_metadata(
            self, app_metadata_key: UnifiedMetadataKey, raw_clean_metadata: RawMetadataDict) -> AppMetadataValue:

        if app_metadata_key == UnifiedMetadataKey.GENRE_NAME:
            return self._get_genre_name_from_raw_clean_metadata_id3v1(
                raw_clean_metadata=raw_clean_metadata, raw_metadata_ket=self.RiffTagKey.GENRE_NAME_OR_CODE)
        else:
            raise MetadataNotSupportedError(f'Metadata key not handled: {app_metadata_key}')

    def _update_not_using_mutagen_metadata(self, app_metadata: AppMetadata):
        """
        Update metadata fields in the RIFF INFO chunk using an optimized chunk-based approach.
        This implementation maintains RIFF specification compliance while providing better
        performance and reliability for metadata updates.

        Note: While TinyTag is excellent for reading metadata, it doesn't support writing.
        Therefore, we implement our own RIFF chunk writer following the specification.
        """
        if not self.metadata_keys_direct_map_write:
            raise ConfigurationError('metadata_keys_direct_map_write must be set')

        # Read the entire file into a mutable bytearray
        self.audio_file.seek(0)
        file_data = bytearray(self.audio_file.read())

        # Skip any ID3v2 tags that might be present
        skipped_data = self._skip_id3v2_tags(bytes(file_data))
        file_data = bytearray(skipped_data)

        # Find RIFF header and validate
        if len(file_data) < 12 or bytes(file_data[:4]) != b'RIFF' or bytes(file_data[8:12]) != b'WAVE':
            raise MetadataNotSupportedError("Invalid WAV file format")

        # Find or create LIST INFO chunk
        info_chunk_start = self._find_info_chunk_in_file_data(file_data)
        if info_chunk_start == -1:
            info_chunk_start = self._create_info_chunk_after_wave_header(file_data)

        # Process metadata updates
        info_chunk_size = int.from_bytes(bytes(file_data[info_chunk_start+4:info_chunk_start+8]), 'little')

        # Build new tags data
        new_tags_data = bytearray()
        for app_key, value in app_metadata.items():
            if value is None or value == "":
                continue

            # Get corresponding RIFF tag
            riff_key = self._get_riff_key_for_metadata(app_key, value)
            if not riff_key:
                continue

            # Prepare tag value
            value_bytes = self._prepare_tag_value(value, app_key)
            if not value_bytes:
                continue

            # Create tag data with proper alignment
            new_tags_data.extend(self._create_aligned_metadata_with_proper_padding(riff_key, value_bytes))

        # Create new INFO chunk
        new_info_chunk = bytearray()
        new_info_chunk.extend(b'LIST')
        new_info_chunk.extend((len(new_tags_data) + 4).to_bytes(4, 'little'))  # +4 for 'INFO'
        new_info_chunk.extend(b'INFO')
        new_info_chunk.extend(new_tags_data)

        # Replace old INFO chunk
        file_data[info_chunk_start:info_chunk_start + info_chunk_size + 8] = new_info_chunk

        # Update RIFF chunk size
        total_size = len(file_data) - 8  # Exclude RIFF and size fields
        file_data[4:8] = total_size.to_bytes(4, 'little')

        # Write updated file
        self.audio_file.seek(0)
        self.audio_file.write(file_data)

    def _find_info_chunk_in_file_data(self, file_data: bytearray) -> int:
        pos = 12  # Start after RIFF header
        while pos < len(file_data) - 8:
            if (bytes(file_data[pos:pos+4]) == b'LIST' and
                pos + 8 < len(file_data) and
                    bytes(file_data[pos+8:pos+12]) == b'INFO'):
                return pos
            chunk_size = int.from_bytes(bytes(file_data[pos+4:pos+8]), 'little')
            pos += 8 + ((chunk_size + 1) & ~1)  # Move to next chunk, maintaining alignment
        return -1

    def _create_info_chunk_after_wave_header(self, file_data: bytearray) -> int:
        info_chunk = bytearray(b'LIST\x04\x00\x00\x00INFO')  # Minimal INFO chunk
        insert_pos = 12  # After RIFF+size+WAVE
        file_data[insert_pos:insert_pos] = info_chunk
        return insert_pos

    def _get_riff_key_for_metadata(self, app_key: UnifiedMetadataKey, value: AppMetadataValue) -> str | None:
        """Get the appropriate RIFF tag key for the metadata."""
        if not self.metadata_keys_direct_map_write:
            return None

        riff_key = self.metadata_keys_direct_map_write.get(app_key)
        if not riff_key:
            if app_key == UnifiedMetadataKey.GENRE_NAME:
                return self.RiffTagKey.GENRE_NAME_OR_CODE
            elif app_key == UnifiedMetadataKey.RATING:
                return self.RiffTagKey.RATING
        return riff_key

    def _prepare_tag_value(self, value: AppMetadataValue, app_key: UnifiedMetadataKey) -> bytes | None:
        """Prepare the tag value for writing, handling special cases."""
        if isinstance(value, list):
            value = value[0] if value else ""

        if app_key == UnifiedMetadataKey.GENRE_NAME:
            value = self._get_genre_code_from_name(str(value))

        if value is None:
            return None

        return str(value).encode('utf-8')

    def _create_aligned_metadata_with_proper_padding(self, metadata_id: str, value_bytes: bytes) -> bytes:
        # Add null terminator
        value_bytes = value_bytes + b'\x00'
        # Pad to even length if needed
        if len(value_bytes) % 2:
            value_bytes = value_bytes + b'\x00'

        return (
            metadata_id.encode('ascii') +
            len(value_bytes).to_bytes(4, 'little') +
            value_bytes
        )

    def _get_genre_code_from_name(self, genre_name: str) -> int | None:
        genre_name_lower = genre_name.lower()
        for code, name in ID3V1_GENRE_CODE_MAP.items():
            if name and name.lower() == genre_name_lower:
                return code
        return 12  # Default to 'Other' genre if not found

    def update_file_metadata(self, app_metadata: AppMetadata):
        """
        Update RIFF metadata in the WAV file.
        
        Args:
            app_metadata: Dictionary containing metadata to update
            
        Raises:
            MetadataNotSupportedError: If unsupported metadata fields are provided
                (e.g., rating, unsupported genre formats)
            FileTypeNotSupportedError: If the file is not a WAV file
            MetadataNotSupportedError: If the file format is invalid or corrupted
        """
        # Check for unsupported metadata fields and raise appropriate exceptions
        # RIFF format has limited metadata support - rating is not supported
        if UnifiedMetadataKey.RATING in app_metadata:
            raise MetadataNotSupportedError(f'{UnifiedMetadataKey.RATING} metadata not supported by RIFF format')
        
        # Call parent method with the original metadata
        super().update_file_metadata(app_metadata)
