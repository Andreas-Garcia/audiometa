import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.wave import WAVE

if TYPE_CHECKING:
    from ...._audio_file import _AudioFile

from ....exceptions import ConfigurationError, FileTypeNotSupportedError, MetadataFieldNotSupportedByMetadataFormatError
from ....utils.id3v1_genre_code_map import ID3V1_GENRE_CODE_MAP
from ....utils.rating_profiles import RatingWriteProfile
from ....utils.types import RawMetadataDict, RawMetadataKey, UnifiedMetadata, UnifiedMetadataValue
from ....utils.unified_metadata_key import UnifiedMetadataKey
from .._RatingSupportingMetadataManager import _RatingSupportingMetadataManager
from ._riff_bext_chunk import (
    extract_bext_chunk,
    find_bext_chunk,
    find_fmt_chunk,
    update_bext_description_in_riff_data,
    update_bext_originator_in_riff_data,
)
from ._riff_constants import (
    RIFF_AUDIO_FORMAT_IEEE_FLOAT,
    RIFF_FORMAT_CHUNK_MIN_SIZE,
    RIFF_HEADER_SIZE,
    RIFF_WAVE_FORMAT_POSITION,
)
from ._riff_file_structure import (
    extract_and_validate_riff_data,
    find_riff_header_after_id3v2,
    get_id3v2_size,
    reconstruct_final_file_data,
    skip_id3v2_tags,
    update_riff_chunk_size,
)
from ._riff_info_chunk import (
    create_aligned_metadata_with_proper_padding,
    create_info_chunk_after_wave_header,
    extract_riff_metadata_directly,
    find_info_chunk_in_file_data,
    update_info_chunk_in_riff_data,
)


class _RiffManager(_RatingSupportingMetadataManager):
    """Manages RIFF metadata for WAV audio files.

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
    1. Text Mode (Preferred when writing): Direct genre name as text
       - Supports any genre name
       - More flexible and readable
       - Better compatibility with modern software
       - Supports custom genres
    2. Genre Code: Uses the standard ID3v1 genre list (0-147)
       - Limited to predefined genres
       - Compatible with older software
       - No custom genres
       - No multiple genres

    Unsupported Metadata:
    RIFF format has limited metadata support compared to other formats. The following metadata fields are NOT supported
    and will raise MetadataFieldNotSupportedByMetadataFormatError if provided:
    - Genre: Limited to predefined genre codes (0-147) or text mode

    Rating Support:
    RIFF format supports rating through the custom IRTD chunk, which is used by some applications
    as an analogy to ID3 tags. While not part of the official RIFF specification, it's widely
    recognized and supported by many audio applications.

    When attempting to update unsupported metadata, the manager will raise
    MetadataFieldNotSupportedByMetadataFormatError with a clear message indicating
    which field is not supported by the RIFF format.

    Note: This manager is the preferred way to handle WAV metadata, as it uses the format's native metadata system
    rather than non-standard alternatives like ID3v2 tags. The custom implementation ensures proper handling of RIFF
    chunk structures, maintaining word alignment and size fields according to the specification.
    """

    class RiffTagKey(RawMetadataKey):
        # Standard
        TITLE = "INAM"
        ARTIST = "IART"
        ALBUM = "IPRD"
        GENRES_NAMES_OR_CODES = "IGNR"
        DATE = "ICRD"  # Creation/Release date
        TRACK_NUMBER = "IPRT"
        COMPOSERS = "ICMP"  # Composers

        # Non-standard
        ALBUM_ARTISTS = "IAAR"
        LANGUAGE = "ILNG"
        RATING = "IRTD"
        COMMENT = "ICMT"
        ENGINEER = "IENG"  # Engineer who worked on the track
        SOFTWARE = "ISFT"  # Software used to create the file
        COPYRIGHT = "ICOP"
        TECHNICIAN = "ITCH"  # Technician who worked on the track
        BPM = "IBPM"
        UNSYNCHRONIZED_LYRICS = "ILYR"

        # BWF
        ISRC = "ISRC"  # International Standard Recording Code
        MBID = "MBID"  # MusicBrainz Track ID (Recording ID)

    def __init__(self, audio_file: "_AudioFile", normalized_rating_max_value: None | int = None):
        # Validate that the file is a WAV file
        if audio_file.file_extension != ".wav":
            msg = f"RiffManager only supports WAV files, got {audio_file.file_extension}"
            raise FileTypeNotSupportedError(msg)

        metadata_keys_direct_map_read: dict[UnifiedMetadataKey, RawMetadataKey | None] = {
            UnifiedMetadataKey.TITLE: self.RiffTagKey.TITLE,
            UnifiedMetadataKey.ARTISTS: self.RiffTagKey.ARTIST,
            UnifiedMetadataKey.ALBUM: self.RiffTagKey.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.RiffTagKey.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: None,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.RiffTagKey.DATE,
            UnifiedMetadataKey.COMPOSERS: self.RiffTagKey.COMPOSERS,
            UnifiedMetadataKey.COPYRIGHT: self.RiffTagKey.COPYRIGHT,
            UnifiedMetadataKey.COMMENT: self.RiffTagKey.COMMENT,
            UnifiedMetadataKey.BPM: self.RiffTagKey.BPM,
            UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: self.RiffTagKey.UNSYNCHRONIZED_LYRICS,
            UnifiedMetadataKey.TRACK_NUMBER: self.RiffTagKey.TRACK_NUMBER,
            UnifiedMetadataKey.ISRC: self.RiffTagKey.ISRC,
            UnifiedMetadataKey.MUSICBRAINZ_TRACKID: self.RiffTagKey.MBID,
            UnifiedMetadataKey.DESCRIPTION: None,
            UnifiedMetadataKey.ORIGINATOR: None,
        }
        metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None] = {
            UnifiedMetadataKey.TITLE: self.RiffTagKey.TITLE,
            UnifiedMetadataKey.ARTISTS: self.RiffTagKey.ARTIST,
            UnifiedMetadataKey.ALBUM: self.RiffTagKey.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.RiffTagKey.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: None,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.RiffTagKey.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.RiffTagKey.DATE,
            UnifiedMetadataKey.COMPOSERS: self.RiffTagKey.COMPOSERS,
            UnifiedMetadataKey.COPYRIGHT: self.RiffTagKey.COPYRIGHT,
            UnifiedMetadataKey.COMMENT: self.RiffTagKey.COMMENT,
            UnifiedMetadataKey.BPM: self.RiffTagKey.BPM,
            UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: self.RiffTagKey.UNSYNCHRONIZED_LYRICS,
            UnifiedMetadataKey.TRACK_NUMBER: self.RiffTagKey.TRACK_NUMBER,
            UnifiedMetadataKey.ISRC: self.RiffTagKey.ISRC,
            UnifiedMetadataKey.MUSICBRAINZ_TRACKID: self.RiffTagKey.MBID,
            UnifiedMetadataKey.DESCRIPTION: None,
            UnifiedMetadataKey.ORIGINATOR: None,
        }
        super().__init__(
            audio_file=audio_file,
            metadata_keys_direct_map_read=metadata_keys_direct_map_read,
            metadata_keys_direct_map_write=metadata_keys_direct_map_write,
            rating_write_profile=RatingWriteProfile.BASE_255_NON_PROPORTIONAL,
            normalized_rating_max_value=normalized_rating_max_value,
            update_using_mutagen_metadata=False,
        )

    def _skip_id3v2_tags(self, data: bytes) -> bytes:
        """Skip ID3v2 tags if present at the start of the file.

        Returns the data starting from after any ID3v2 tags.
        """
        return skip_id3v2_tags(data)

    def _extract_riff_metadata_directly(self, file_data: bytes) -> dict[str, list[str]]:
        """Manually extract metadata from RIFF chunks without relying on external libraries.

        This method directly parses the RIFF structure to extract metadata from the INFO chunk.
        """
        return extract_riff_metadata_directly(file_data, self._skip_id3v2_tags, self.RiffTagKey)

    def _extract_bext_chunk(self, file_data: bytes) -> dict[str, Any] | None:
        """Extract and parse the bext chunk from BWF files."""
        return extract_bext_chunk(file_data, self._skip_id3v2_tags)

    @contextlib.contextmanager
    def _suppress_output(self) -> Any:
        """Context manager to suppress all output including direct prints."""
        with (
            Path(os.devnull).open("w") as devnull,
            contextlib.redirect_stdout(devnull),
            contextlib.redirect_stderr(devnull),
        ):
            yield

    def _extract_mutagen_metadata(self) -> RawMetadataDict:
        """Extract RIFF metadata from WAV files using direct RIFF chunk parsing.

        This method reads the WAV file's INFO chunk directly, providing the most reliable way to access RIFF metadata.
        """
        self.audio_file.seek(0)
        file_data = self.audio_file.read()

        # Skip ID3v2 metadata if present and create a clean RIFF file for mutagen
        clean_data = self._skip_id3v2_tags(file_data)

        # Create a temporary file with just the RIFF data for mutagen to parse
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(clean_data)
            temp_file.flush()

            try:
                # Create WAVE object with the clean RIFF data
                wave = WAVE(filename=temp_file.name)
                info_tags = self._extract_riff_metadata_directly(file_data)  # Use original data for our custom parsing
                wave.info = info_tags
                return cast(RawMetadataDict, wave)
            finally:
                # Clean up temporary file

                with contextlib.suppress(OSError):
                    Path(temp_file.name).unlink()

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
        self, raw_mutagen_metadata: MutagenMetadata
    ) -> RawMetadataDict:
        """Convert RIFF metadata to dictionary.

        Extracts tags from our custom info_tags attribute which contains the directly parsed INFO chunk data.
        """
        raw_mutagen_metadata_wav: WAVE = cast(WAVE, raw_mutagen_metadata)
        raw_metadata_dict: dict = {}

        # Get metadata from our custom info which contains the directly parsed INFO chunk
        if hasattr(raw_mutagen_metadata_wav, "info") and raw_mutagen_metadata_wav.info is not None:
            info_tags = raw_mutagen_metadata_wav.info
            for key, value in info_tags.items():
                # key is a FourCC string; check against enum member values
                if any(key == member.value for member in self.RiffTagKey.__members__.values()):
                    # info_tags now contains lists of values, so we can pass them directly
                    raw_metadata_dict[key] = value

        return raw_metadata_dict

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        # raw_clean_metadata uses FourCC string keys; compare using enum .value
        rating_key = self.RiffTagKey.RATING
        if rating_key not in raw_clean_metadata:
            return None, False

        raw_ratings = raw_clean_metadata[rating_key]
        if not raw_ratings or len(raw_ratings) == 0:
            return None, False

        raw_rating = raw_ratings[0]
        # It is a Traktor rating if it's an integer
        if isinstance(raw_rating, str):
            return int(raw_rating), False
        return cast(int, raw_rating), True

    def _get_undirectly_mapped_metadata_value_other_than_rating_from_raw_clean_metadata(
        self, raw_clean_metadata: RawMetadataDict, unified_metadata_key: UnifiedMetadataKey
    ) -> UnifiedMetadataValue:
        if unified_metadata_key == UnifiedMetadataKey.GENRES_NAMES:
            return self._get_genres_from_raw_clean_metadata_uppercase_keys(
                raw_clean_metadata, self.RiffTagKey.GENRES_NAMES_OR_CODES
            )
        if unified_metadata_key == UnifiedMetadataKey.DESCRIPTION:
            # Read from bext chunk
            try:
                self.audio_file.seek(0)
                file_data = self.audio_file.read()
                bext_data = self._extract_bext_chunk(file_data)
                if bext_data and "Description" in bext_data:
                    return cast(str, bext_data["Description"])
            except Exception:
                pass
            return None
        if unified_metadata_key == UnifiedMetadataKey.ORIGINATOR:
            # Read from bext chunk
            try:
                self.audio_file.seek(0)
                file_data = self.audio_file.read()
                bext_data = self._extract_bext_chunk(file_data)
                if bext_data and "Originator" in bext_data:
                    return cast(str, bext_data["Originator"])
            except Exception:
                pass
            return None
        msg = f"Metadata key not handled: {unified_metadata_key}"
        raise MetadataFieldNotSupportedByMetadataFormatError(msg)

    def _update_not_using_mutagen_metadata(self, unified_metadata: UnifiedMetadata) -> None:
        """Update metadata fields in the RIFF INFO chunk using an optimized chunk-based approach.

        This implementation
        maintains RIFF specification compliance while providing better performance and reliability for metadata updates.

        Note: While TinyTag is excellent for reading metadata, it doesn't support writing.
        Therefore, we implement our own RIFF chunk writer following the specification.
        """
        self._validate_metadata_for_riff_update(unified_metadata)

        file_data, should_preserve_id3v2 = self._read_file_data_for_update()
        riff_data = self._extract_and_validate_riff_data(file_data, should_preserve_id3v2)

        info_chunk_start = self._ensure_info_chunk_exists(riff_data)
        merged_metadata = self._merge_existing_and_new_metadata(riff_data, unified_metadata)

        new_tags_data = self._build_info_chunk_tags_data(merged_metadata)
        self._update_info_chunk_in_riff_data(riff_data, info_chunk_start, new_tags_data)

        self._update_bext_fields_in_riff_data(riff_data, merged_metadata)
        self._update_riff_chunk_size(riff_data)

        final_file_data = self._reconstruct_final_file_data(file_data, riff_data, should_preserve_id3v2)
        self._write_file_and_clear_cache(final_file_data)

    def _validate_metadata_for_riff_update(self, unified_metadata: UnifiedMetadata) -> None:
        """Validate that all metadata fields are supported by RIFF format."""
        if not self.metadata_keys_direct_map_write:
            msg = "metadata_keys_direct_map_write must be set"
            raise ConfigurationError(msg)

        for unified_metadata_key in unified_metadata:
            if unified_metadata_key not in self.metadata_keys_direct_map_write:
                msg = f"{unified_metadata_key} metadata not supported by RIFF format"
                raise MetadataFieldNotSupportedByMetadataFormatError(msg)

    def _read_file_data_for_update(self) -> tuple[bytearray, bool]:
        """Read file data and determine ID3v2 preservation strategy.

        Returns:
            Tuple of (file_data, should_preserve_id3v2)
        """
        self.audio_file.seek(0)
        file_data = bytearray(self.audio_file.read())

        should_preserve_id3v2 = self._should_preserve_id3v2_tags()

        if not should_preserve_id3v2:
            # For other strategies (CLEANUP, SYNC), strip ID3v2 tags
            skipped_data = self._skip_id3v2_tags(bytes(file_data))
            file_data = bytearray(skipped_data)

        return file_data, should_preserve_id3v2

    def _extract_and_validate_riff_data(self, file_data: bytearray, should_preserve_id3v2: bool) -> bytearray:
        """Extract RIFF data from file data and validate format.

        Args:
            file_data: Full file data including potential ID3v2 tags
            should_preserve_id3v2: Whether to preserve ID3v2 tags

        Returns:
            RIFF data bytearray

        Raises:
            MetadataFieldNotSupportedByMetadataFormatError: If RIFF format is invalid
        """
        return extract_and_validate_riff_data(file_data, should_preserve_id3v2, self._find_riff_header_after_id3v2)

    def _ensure_info_chunk_exists(self, riff_data: bytearray) -> int:
        """Find or create LIST INFO chunk in RIFF data.

        Args:
            riff_data: RIFF data bytearray

        Returns:
            Start position of INFO chunk
        """
        info_chunk_start = find_info_chunk_in_file_data(riff_data)
        if info_chunk_start == -1:
            info_chunk_start = create_info_chunk_after_wave_header(riff_data)
        return info_chunk_start

    def _merge_existing_and_new_metadata(
        self, riff_data: bytearray, unified_metadata: UnifiedMetadata
    ) -> UnifiedMetadata:
        """Read existing metadata and merge with new metadata.

        Args:
            riff_data: RIFF data bytearray
            unified_metadata: New metadata to merge

        Returns:
            Merged metadata (new metadata takes precedence)
        """
        if not self.metadata_keys_direct_map_write:
            msg = "metadata_keys_direct_map_write must be set"
            raise ConfigurationError(msg)

        existing_metadata = self._extract_riff_metadata_directly(bytes(riff_data))

        # Convert existing metadata to unified format
        existing_unified_metadata: UnifiedMetadata = {}
        for existing_riff_key, values in existing_metadata.items():
            # Find the corresponding unified metadata key
            for unified_key, mapped_riff_key in self.metadata_keys_direct_map_write.items():
                if mapped_riff_key and mapped_riff_key.value == existing_riff_key:
                    if len(values) == 1:
                        existing_unified_metadata[unified_key] = values[0]
                    else:
                        existing_unified_metadata[unified_key] = values
                    break

        # Merge existing metadata with new metadata (new metadata takes precedence)
        return {**existing_unified_metadata, **unified_metadata}

    def _build_info_chunk_tags_data(self, merged_metadata: UnifiedMetadata) -> bytearray:
        """Build new INFO chunk tags data from merged metadata.

        Args:
            merged_metadata: Merged metadata to convert to RIFF tags

        Returns:
            Bytearray containing INFO chunk tags data
        """
        new_tags_data = bytearray()
        for app_key, value in merged_metadata.items():
            if value is None or value == "":
                continue

            # Get corresponding RIFF tag
            riff_key: RawMetadataKey | None = self._get_riff_key_for_metadata(app_key, value)
            if not riff_key:
                continue

            # Handle multiple values (e.g., multiple artists)
            if isinstance(value, list):
                # Values are already filtered at the base level
                if value:
                    # Use smart separator to concatenate multiple values
                    separator = self.find_safe_separator(value)
                    concatenated_value: str = separator.join(value)
                    value_bytes = self._prepare_tag_value(concatenated_value, app_key)
                    if value_bytes:
                        new_tags_data.extend(create_aligned_metadata_with_proper_padding(riff_key, value_bytes))
            # Single value - ensure it's not None before processing
            elif isinstance(value, int | float | str):
                value_bytes = self._prepare_tag_value(value, app_key)
                if value_bytes:
                    new_tags_data.extend(create_aligned_metadata_with_proper_padding(riff_key, value_bytes))

        return new_tags_data

    def _update_info_chunk_in_riff_data(
        self, riff_data: bytearray, info_chunk_start: int, new_tags_data: bytearray
    ) -> None:
        """Update INFO chunk in RIFF data with new tags.

        Args:
            riff_data: RIFF data bytearray (modified in-place)
            info_chunk_start: Start position of existing INFO chunk
            new_tags_data: New tags data to write
        """
        update_info_chunk_in_riff_data(riff_data, info_chunk_start, new_tags_data)

    def _update_bext_fields_in_riff_data(self, riff_data: bytearray, merged_metadata: UnifiedMetadata) -> None:
        """Update bext chunk fields (like DESCRIPTION) in RIFF data.

        Args:
            riff_data: RIFF data bytearray (modified in-place)
            merged_metadata: Merged metadata containing bext fields
        """
        if UnifiedMetadataKey.DESCRIPTION in merged_metadata:
            description_value = merged_metadata[UnifiedMetadataKey.DESCRIPTION]
            update_bext_description_in_riff_data(riff_data, cast(str | None, description_value))
        if UnifiedMetadataKey.ORIGINATOR in merged_metadata:
            originator_value = merged_metadata[UnifiedMetadataKey.ORIGINATOR]
            update_bext_originator_in_riff_data(riff_data, cast(str | None, originator_value))

    def _update_riff_chunk_size(self, riff_data: bytearray) -> None:
        """Update RIFF chunk size in RIFF data.

        Args:
            riff_data: RIFF data bytearray (modified in-place)
        """
        update_riff_chunk_size(riff_data)

    def _reconstruct_final_file_data(
        self, file_data: bytearray, riff_data: bytearray, should_preserve_id3v2: bool
    ) -> bytearray:
        """Reconstruct final file data with ID3v2 tags if needed.

        Args:
            file_data: Original file data
            riff_data: Updated RIFF data
            should_preserve_id3v2: Whether ID3v2 tags should be preserved

        Returns:
            Final file data ready to write
        """
        return reconstruct_final_file_data(file_data, riff_data, should_preserve_id3v2, self._get_id3v2_size)

    def _write_file_and_clear_cache(self, final_file_data: bytearray) -> None:
        """Write final file data and clear cached metadata.

        Args:
            final_file_data: Final file data to write
        """
        self.audio_file.seek(0)
        self.audio_file.write(final_file_data)

        # Clear cached metadata to ensure subsequent reads reflect the changes
        self.raw_clean_metadata = None
        self.raw_clean_metadata_uppercase_keys = None
        self.raw_mutagen_metadata = None

    def _find_bext_chunk(self, file_data: bytes) -> int:
        """Find the position of the bext chunk."""
        return find_bext_chunk(file_data, self._skip_id3v2_tags)

    def _find_fmt_chunk(self, file_data: bytes) -> int:
        """Find the position of the fmt chunk."""
        return find_fmt_chunk(file_data, self._skip_id3v2_tags)

    def delete_metadata(self) -> bool:
        """Delete all RIFF metadata from the audio file.

        This removes all RIFF INFO chunks from the file while preserving the audio data.
        Uses custom RIFF chunk manipulation since mutagen doesn't support RIFF writing.

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Read the entire file into a mutable bytearray
            self.audio_file.seek(0)
            file_data = bytearray(self.audio_file.read())

            # Check if we should preserve ID3v2 tags
            should_preserve_id3v2 = self._should_preserve_id3v2_tags()

            # Extract and validate RIFF data
            try:
                riff_data = extract_and_validate_riff_data(
                    file_data, should_preserve_id3v2, self._find_riff_header_after_id3v2
                )
            except MetadataFieldNotSupportedByMetadataFormatError:
                return False  # Invalid RIFF format

            # Find and remove LIST INFO chunk
            info_chunk_start = find_info_chunk_in_file_data(riff_data)
            if info_chunk_start == -1:
                return True  # No INFO chunk found, consider deletion successful

            # Get the size of the INFO chunk
            info_chunk_size = int.from_bytes(bytes(riff_data[info_chunk_start + 4 : info_chunk_start + 8]), "little")

            # Remove the INFO chunk
            riff_data[info_chunk_start : info_chunk_start + info_chunk_size + 8] = b""

            # Update RIFF chunk size
            update_riff_chunk_size(riff_data)

            # If we preserved ID3v2 tags, reconstruct the full file
            final_file_data = reconstruct_final_file_data(
                file_data, riff_data, should_preserve_id3v2, self._get_id3v2_size
            )

            # Write updated file
            self.audio_file.seek(0)
            self.audio_file.write(final_file_data)
        except Exception:
            return False
        else:
            return True

    def _get_riff_key_for_metadata(
        self, app_key: UnifiedMetadataKey, _value: UnifiedMetadataValue
    ) -> RawMetadataKey | None:
        """Get the appropriate RIFF tag key for the metadata."""
        if not self.metadata_keys_direct_map_write:
            return None

        riff_key = self.metadata_keys_direct_map_write.get(app_key, None)
        if not riff_key:
            if app_key == UnifiedMetadataKey.GENRES_NAMES:
                return cast(RawMetadataKey | None, self.RiffTagKey.GENRES_NAMES_OR_CODES)
            if app_key == UnifiedMetadataKey.RATING:
                return cast(RawMetadataKey | None, self.RiffTagKey.RATING)
        return riff_key

    def _prepare_tag_value(self, value: UnifiedMetadataValue, app_key: UnifiedMetadataKey) -> bytes | None:
        """Prepare the tag value for writing, handling special cases."""
        # Handle list values (should not happen in this method anymore due to upstream processing)
        if isinstance(value, list):
            value = value[0] if value else ""

        if app_key == UnifiedMetadataKey.GENRES_NAMES:
            # Write genre as text instead of numeric code for better compatibility
            value = str(value)
        elif (
            app_key == UnifiedMetadataKey.RATING and value is not None and self.normalized_rating_max_value is not None
        ):
            # Convert normalized rating to file rating for RIFF format
            try:
                # Preserve float values to support half-star ratings (consistent with classic star rating systems)
                normalized_rating = float(value)
                file_rating = self._convert_normalized_rating_to_file_rating(normalized_rating=normalized_rating)
                value = file_rating
            except (TypeError, ValueError):
                # If conversion fails, use the original value
                pass

        if value is None:
            return None

        return str(value).encode("utf-8")

    def _create_aligned_metadata_with_proper_padding(self, metadata_id: RawMetadataKey, value_bytes: bytes) -> bytes:
        return create_aligned_metadata_with_proper_padding(metadata_id, value_bytes)

    def _get_genre_code_from_name(self, genre_name: str) -> int | None:
        genre_name_lower = genre_name.lower()
        for code, name in ID3V1_GENRE_CODE_MAP.items():
            if name and name.lower() == genre_name_lower:
                return cast(int | None, code)
        return cast(int | None, 12)  # Default to 'Other' genre if not found

    def _should_preserve_id3v2_tags(self) -> bool:
        """Determine if ID3v2 tags should be preserved based on the calling context and file state.

        This method detects if the RIFF manager is being called in a PRESERVE strategy
        context by checking the call stack. In PRESERVE strategy, the high-level
        _handle_metadata_strategy function will restore ID3v2 metadata after RIFF
        writing, so we should not strip it.

        We preserve ID3v2 tags when:
        1. We're in a PRESERVE strategy context AND we're writing to RIFF format
        2. We're in a SYNC strategy context AND we're writing to RIFF format
        3. ID3v2 tags exist in the file (for coexistence support)
        """
        import inspect

        # First, check if ID3v2 tags exist in the file
        # This allows coexistence even when not in a strategy context
        try:
            with Path(self.audio_file.file_path).open("rb") as f:
                first_bytes = f.read(10)
                if first_bytes.startswith(b"ID3"):
                    # ID3v2 tags exist, preserve them for coexistence
                    return True
        except Exception:
            # If we can't read the file, fall back to strategy detection
            pass

        # Get the call stack
        frame = inspect.currentframe()
        try:
            # Look for _handle_metadata_strategy in the call stack
            while frame:
                if (
                    frame.f_code.co_name == "_handle_metadata_strategy"
                    and "strategy" in frame.f_locals
                    and "target_format_actual" in frame.f_locals
                ):
                    # Check if we're in the PRESERVE strategy branch
                    # Look at the local variables to determine the strategy and target format
                    strategy = frame.f_locals["strategy"]
                    target_format = frame.f_locals["target_format_actual"]
                    from audiometa.utils.metadata_format import MetadataFormat
                    from audiometa.utils.metadata_writing_strategy import MetadataWritingStrategy

                    # Preserve ID3v2 tags when:
                    # 1. PRESERVE strategy and target format is RIFF (preserve existing ID3v2 tags)
                    # 2. SYNC strategy and target format is RIFF
                    #    (preserve ID3v2 tags that were written by other managers)
                    if strategy in (MetadataWritingStrategy.PRESERVE, MetadataWritingStrategy.SYNC):
                        return bool(target_format == MetadataFormat.RIFF)
                    return False
                frame = frame.f_back
        finally:
            del frame

        # Default to not preserving (for backward compatibility)
        return False

    def _find_riff_header_after_id3v2(self, file_data: bytearray) -> int:
        """Find the RIFF header after ID3v2 tags in the file data.

        Returns the position of the RIFF header or -1 if not found.
        """
        return find_riff_header_after_id3v2(file_data)

    def _get_id3v2_size(self, file_data: bytearray) -> int:
        """Get the size of ID3v2 tags at the beginning of the file.

        Returns the total size including header and data.
        """
        return get_id3v2_size(file_data)

    def get_header_info(self) -> dict:
        try:
            # Read file data to analyze RIFF structure
            self.audio_file.seek(0)
            file_data = self.audio_file.read()

            if (
                len(file_data) < RIFF_HEADER_SIZE
                or not file_data.startswith(b"RIFF")
                or file_data[RIFF_WAVE_FORMAT_POSITION:RIFF_HEADER_SIZE] != b"WAVE"
            ):
                return {"present": False, "chunk_info": {}}

            # Parse RIFF chunk info
            riff_chunk_size = int.from_bytes(file_data[4:8], "little")
            info_chunk_size = 0
            audio_format = "Unknown"
            subchunk_size = 0

            # Find INFO chunk
            pos = 12
            while pos < len(file_data) - 8:
                chunk_id = file_data[pos : pos + 4]
                chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")

                if chunk_id == b"LIST" and file_data[pos + 8 : pos + 12] == b"INFO":
                    info_chunk_size = chunk_size
                    break
                if chunk_id == b"fmt ":
                    # Parse format chunk
                    if chunk_size >= RIFF_FORMAT_CHUNK_MIN_SIZE:
                        audio_format_code = int.from_bytes(file_data[pos + 8 : pos + 10], "little")
                        if audio_format_code == 1:
                            audio_format = "PCM"
                        elif audio_format_code == RIFF_AUDIO_FORMAT_IEEE_FLOAT:
                            audio_format = "IEEE Float"
                        else:
                            audio_format = f"Code {audio_format_code}"
                elif chunk_id == b"data":
                    subchunk_size = chunk_size
                    break

                pos += 8 + chunk_size
                if chunk_size % 2 == 1:  # Word alignment
                    pos += 1
        except Exception:
            return {"present": False, "chunk_info": {}}
        else:
            return {
                "present": True,
                "chunk_info": {
                    "riff_chunk_size": riff_chunk_size,
                    "info_chunk_size": info_chunk_size,
                    "audio_format": audio_format,
                    "subchunk_size": subchunk_size,
                },
            }

    def get_raw_metadata_info(self) -> dict[str, Any]:
        try:
            if self.raw_clean_metadata is None:
                extracted_metadata: RawMetadataDict = self._extract_cleaned_raw_metadata_from_file()
                self.raw_clean_metadata = extracted_metadata

            if not self.raw_clean_metadata:
                # Still try to extract bext chunk even if no INFO metadata
                chunk_structure = {}
                try:
                    self.audio_file.seek(0)
                    file_data = self.audio_file.read()
                    bext_data = self._extract_bext_chunk(file_data)
                    if bext_data:
                        chunk_structure["bext"] = bext_data
                except Exception:
                    pass

                return {
                    "raw_data": None,
                    "parsed_fields": {},
                    "frames": {},
                    "comments": {},
                    "chunk_structure": chunk_structure,
                }

            raw_clean_metadata: RawMetadataDict = self.raw_clean_metadata

            # Get parsed fields
            parsed_fields = {}
            for key, value in raw_clean_metadata.items():
                parsed_fields[key] = value[0] if value else ""

            # Extract bext chunk
            chunk_structure = {}
            try:
                self.audio_file.seek(0)
                file_data = self.audio_file.read()
                bext_data = self._extract_bext_chunk(file_data)
                if bext_data:
                    chunk_structure["bext"] = bext_data
            except Exception:
                pass
        except Exception:
            return {"raw_data": None, "parsed_fields": {}, "frames": {}, "comments": {}, "chunk_structure": {}}
        else:
            return {
                "raw_data": None,  # RIFF data is complex binary structure
                "parsed_fields": parsed_fields,
                "frames": {},
                "comments": {},
                "chunk_structure": chunk_structure,
            }
