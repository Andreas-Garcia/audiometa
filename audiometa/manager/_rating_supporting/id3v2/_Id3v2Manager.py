from typing import TYPE_CHECKING, ClassVar, cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.id3 import ID3
from mutagen.id3._frames import (
    COMM,
    POPM,
    TALB,
    TBPM,
    TCOM,
    TCON,
    TCOP,
    TDAT,
    TDRC,
    TDRL,
    TENC,
    TIT2,
    TKEY,
    TLAN,
    TMOO,
    TPE1,
    TPE2,
    TPOS,
    TPUB,
    TRCK,
    TSRC,
    TYER,
    USLT,
    WOAR,
)
from mutagen.id3._util import ID3NoHeaderError

from audiometa.utils.disc_number_read import parse_disc_number_from_combined_str, parse_disc_total_from_combined_str
from audiometa.utils.raw_metadata_sanitizer import sanitize_id3v2_raw_info
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

if TYPE_CHECKING:
    from ...._audio_file import _AudioFile
from ....exceptions import MetadataFieldNotSupportedByMetadataFormatError
from ....utils.rating_profiles import RatingWriteProfile
from ....utils.types import RawMetadataDict, RawMetadataKey, UnifiedMetadata, UnifiedMetadataValue
from .._RatingSupportingMetadataManager import _RatingSupportingMetadataManager


class _Id3v2Manager(_RatingSupportingMetadataManager):
    """ID3v2 metadata manager for audio files.

    ID3v2 Version Compatibility Table:
    +---------------+----------+----------+----------+
    | Player/Device | ID3v2.2  | ID3v2.3  | ID3v2.4  |
    +---------------+----------+----------+----------+
    | Windows Media Player                           |
    |  - WMP 9-12   |    ✓     |    ✓     |    ~     |
    |  - WMP 7-8    |    ✓     |    ✓     |          |
    +---------------+----------+----------+----------+
    | iTunes                                         |
    |  - 12.x+      |    ✓     |    ✓     |    ✓     |
    |  - 7.x-11.x   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Winamp                                         |
    |  - 5.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x-4.x    |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | MusicBee                                       |
    |  - 3.x+       |    ✓     |    ✓     |    ✓     |
    |  - 2.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | VLC                                            |
    |  - 2.x+       |    ✓     |    ✓     |    ✓     |
    |  - 1.x        |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smartphones                                    |
    |  - iOS 7+     |    ✓     |    ✓     |    ✓     |
    |  - Android 4+ |    ✓     |    ✓     |    ✓     |
    |  - Windows    |    ✓     |    ✓     |    ✓     |
    |  - Blackberry |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Network Players                                |
    |  - Sonos      |    ✓     |    ✓     |    ✓     |
    |  - Roku       |    ✓     |    ✓     |    ~     |
    |  - Chromecast |    ✓     |    ✓     |    ✓     |
    |  - Apple TV   |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    |iPods/MP3 Players                               |
    |  - iPod 5G+   |    ✓     |    ✓     |    ✓     |
    |  - iPod 1-4G  |    ✓     |    ✓     |    ~     |
    |  - Zune       |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Car Systems                                    |
    |  - Post-2010  |    ✓     |    ✓     |    ~     |
    |  - Pre-2010   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | Home Audio Systems                             |
    |  - Post-2000  |    ✓     |    ✓     |    ~     |
    |  - Pre-2000   |    ✓     |    ~     |          |
    +---------------+----------+----------+----------+
    | DJ Software                                    |
    |  - Traktor    |    ✓     |    ✓     |    ✓     |
    |  - Serato     |    ✓     |    ✓     |    ~     |
    |  - VirtualDJ  |    ✓     |    ✓     |    ~     |
    |  - Rekordbox  |    ✓     |    ✓     |    ~     |
    |  - Mixxx      |    ✓     |    ✓     |    ~     |
    |  - Cross DJ   |    ✓     |    ✓     |    ~     |
    |  - djay Pro   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Web Browsers                                   |
    |  - Chrome     |    ✓     |    ✓     |    ✓     |
    |  - Firefox    |    ✓     |    ✓     |    ✓     |
    |  - Safari     |    ✓     |    ✓     |    ✓     |
    |  - Edge       |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+
    | Gaming Consoles                                |
    |  - PS4/PS5    |    ✓     |    ✓     |    ✓     |
    |  - Xbox Series|    ✓     |    ✓     |    ✓     |
    |  - PS3        |    ✓     |    ✓     |    ~     |
    |  - Xbox 360   |    ✓     |    ✓     |    ~     |
    +---------------+----------+----------+----------+
    | Smart TVs                                      |
    |  - Samsung    |    ✓     |    ✓     |    ~     |
    |  - LG         |    ✓     |    ✓     |    ~     |
    |  - Sony       |    ✓     |    ✓     |    ~     |
    |  - Android TV |    ✓     |    ✓     |    ✓     |
    +---------------+----------+----------+----------+

    Legend:
    ✓ = Full support
    ~ = Partial support/May have issues
      = No support

    Notes:
    - ID3v2.4 introduced UTF-8 encoding and unsync changes
    - Older players may have issues with ID3v2.4's changes
    - For maximum compatibility, ID3v2.3 is recommended

    - ID3:
        - Writing Policy:
            * The app writes ID3v2 tags in the specified version (default: v2.3)
            * When updating an existing file:
                - Tags are upgraded to the specified version if different
                - v2.2, v2.3, or v2.4 tags are upgraded to the specified version
                - Frame IDs are automatically converted
                - All text is encoded in UTF-8
            * Reading supports all versions (v2.2, v2.3, v2.4)
            * Only one ID3v2 version can exist in a file at a time
            * Native format for MP3 files
            * Version selection allows choosing between v2.3 (maximum compatibility) and v2.4 (modern features)

        - ID3v1:
            * Fixed 128-byte format at end of file
            * ASCII only, no Unicode
            * Limited to 30 chars for text fields
            * Single byte for track number (v1.1 only)
            * Genre limited to predefined codes (0-147)
            * Legacy format

        - ID3v2:
            * v2.2:
                - Introduced in 1998
                - Three-character frame IDs (TT2, TP1, etc.)
                - ISO-8859-1 or UCS-2 text encoding
                - All standard fields supported
                - Simpler header structure than v2.3/v2.4
                - Basic support for embedded images
                - Less common but equally functional

            * v2.3:
                - Introduced in 1999
                - TYER+TDAT frames for date (year and date separately)
                - UTF-16/UTF-16BE text encoding
                - Basic unsynchronization
                - All metadata fields supported
                - Better support for embedded images and other binary data
                - Most widely used version

            * v2.4:
                - Introduced in 2000
                - TDRC frame for full timestamps (YYYY-MM-DD)
                - UTF-8 text encoding
                - Extended header features
                - Unsynchronization per frame
                - All metadata fields supported
                - New frames for more detailed metadata (e.g., TDRC for recording time, TDRL for release time)
                - Preferred version for new tags

    For maximum compatibility, ID3v2.3 is used as the default version for writing metadata.
    Users can choose ID3v2.4 for modern features if their target players support it.
    When reading/updating an existing file, the ID3 tags will be updated to the specified version format.
    """

    ID3_RATING_APP_EMAIL = "audiometa-python@audiometa.dev"

    class Id3TextFrame(RawMetadataKey):
        TITLE = "TIT2"
        ARTISTS = "TPE1"
        ALBUM = "TALB"
        ALBUM_ARTISTS = "TPE2"
        GENRES_NAMES = "TCON"

        # In cleaned metadata, the rating is stored as a tuple the potential identifier (e.g. 'Traktor') and the rating
        # value
        RATING = "POPM"
        LANGUAGE = "TLAN"
        RECORDING_TIME = "TDRC"  # ID3v2.4 recording time
        RELEASE_TIME = "TDRL"  # ID3v2.4 release time
        YEAR = "TYER"  # ID3v2.3 year
        DATE = "TDAT"  # ID3v2.3 date (DDMM)
        TRACK_NUMBER = "TRCK"
        DISC_NUMBER = "TPOS"
        BPM = "TBPM"

        # Additional metadata fields
        COMPOSERS = "TCOM"
        PUBLISHER = "TPUB"
        COPYRIGHT = "TCOP"
        UNSYNCHRONIZED_LYRICS = "USLT"
        COMMENT = "COMM"  # Comment frame
        ENCODER = "TENC"
        URL = "WOAR"  # Official artist/performer webpage
        ISRC = "TSRC"
        MOOD = "TMOO"
        KEY = "TKEY"
        REPLAYGAIN = "REPLAYGAIN"

    ID3_TEXT_FRAME_CLASS_MAP: ClassVar[dict[RawMetadataKey, type]] = {
        Id3TextFrame.TITLE: TIT2,
        Id3TextFrame.ARTISTS: TPE1,
        Id3TextFrame.ALBUM: TALB,
        Id3TextFrame.ALBUM_ARTISTS: TPE2,
        Id3TextFrame.GENRES_NAMES: TCON,
        Id3TextFrame.LANGUAGE: TLAN,
        Id3TextFrame.RECORDING_TIME: TDRC,
        Id3TextFrame.RELEASE_TIME: TDRL,
        Id3TextFrame.YEAR: TYER,
        Id3TextFrame.DATE: TDAT,
        Id3TextFrame.TRACK_NUMBER: TRCK,
        Id3TextFrame.DISC_NUMBER: TPOS,
        Id3TextFrame.BPM: TBPM,
        Id3TextFrame.RATING: POPM,
        Id3TextFrame.COMPOSERS: TCOM,
        Id3TextFrame.PUBLISHER: TPUB,
        Id3TextFrame.COPYRIGHT: TCOP,
        Id3TextFrame.UNSYNCHRONIZED_LYRICS: USLT,
        Id3TextFrame.COMMENT: COMM,
        Id3TextFrame.ENCODER: TENC,
        Id3TextFrame.URL: WOAR,
        Id3TextFrame.ISRC: TSRC,
        Id3TextFrame.MOOD: TMOO,
        Id3TextFrame.KEY: TKEY,
    }

    def __init__(
        self,
        audio_file: "_AudioFile",
        normalized_rating_max_value: int | None = None,
        id3v2_version: tuple[int, int, int] = (2, 3, 0),
    ):
        self.id3v2_version = id3v2_version
        metadata_keys_direct_map_read = {
            UnifiedMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            UnifiedMetadataKey.ARTISTS: self.Id3TextFrame.ARTISTS,
            UnifiedMetadataKey.ALBUM: self.Id3TextFrame.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.Id3TextFrame.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: self.Id3TextFrame.GENRES_NAMES,
            UnifiedMetadataKey.RATING: None,
            UnifiedMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.Id3TextFrame.RECORDING_TIME,
            UnifiedMetadataKey.TRACK_NUMBER: self.Id3TextFrame.TRACK_NUMBER,
            UnifiedMetadataKey.DISC_NUMBER: None,
            UnifiedMetadataKey.DISC_TOTAL: None,
            UnifiedMetadataKey.BPM: self.Id3TextFrame.BPM,
            UnifiedMetadataKey.COMPOSERS: self.Id3TextFrame.COMPOSERS,
            UnifiedMetadataKey.PUBLISHER: self.Id3TextFrame.PUBLISHER,
            UnifiedMetadataKey.COPYRIGHT: self.Id3TextFrame.COPYRIGHT,
            UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: self.Id3TextFrame.UNSYNCHRONIZED_LYRICS,
            UnifiedMetadataKey.COMMENT: self.Id3TextFrame.COMMENT,
            UnifiedMetadataKey.REPLAYGAIN: None,
            UnifiedMetadataKey.ISRC: self.Id3TextFrame.ISRC,
            UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None,
            UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None,
        }
        metadata_keys_direct_map_write: dict[UnifiedMetadataKey, RawMetadataKey | None] = {
            UnifiedMetadataKey.TITLE: self.Id3TextFrame.TITLE,
            UnifiedMetadataKey.ARTISTS: self.Id3TextFrame.ARTISTS,
            UnifiedMetadataKey.ALBUM: self.Id3TextFrame.ALBUM,
            UnifiedMetadataKey.ALBUM_ARTISTS: self.Id3TextFrame.ALBUM_ARTISTS,
            UnifiedMetadataKey.GENRES_NAMES: self.Id3TextFrame.GENRES_NAMES,
            UnifiedMetadataKey.RATING: self.Id3TextFrame.RATING,
            UnifiedMetadataKey.LANGUAGE: self.Id3TextFrame.LANGUAGE,
            UnifiedMetadataKey.RELEASE_DATE: self.Id3TextFrame.RECORDING_TIME,
            UnifiedMetadataKey.TRACK_NUMBER: self.Id3TextFrame.TRACK_NUMBER,
            UnifiedMetadataKey.DISC_NUMBER: None,
            UnifiedMetadataKey.DISC_TOTAL: None,
            UnifiedMetadataKey.BPM: self.Id3TextFrame.BPM,
            UnifiedMetadataKey.COMPOSERS: self.Id3TextFrame.COMPOSERS,
            UnifiedMetadataKey.PUBLISHER: self.Id3TextFrame.PUBLISHER,
            UnifiedMetadataKey.COPYRIGHT: self.Id3TextFrame.COPYRIGHT,
            UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: self.Id3TextFrame.UNSYNCHRONIZED_LYRICS,
            UnifiedMetadataKey.COMMENT: self.Id3TextFrame.COMMENT,
            UnifiedMetadataKey.REPLAYGAIN: None,
            UnifiedMetadataKey.ISRC: self.Id3TextFrame.ISRC,
            UnifiedMetadataKey.MUSICBRAINZ_TRACKID: None,
            UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS: None,
        }

        super().__init__(
            audio_file=audio_file,
            metadata_keys_direct_map_read=cast(
                dict[UnifiedMetadataKey, RawMetadataKey | None], metadata_keys_direct_map_read
            ),
            metadata_keys_direct_map_write=metadata_keys_direct_map_write,
            rating_write_profile=RatingWriteProfile.BASE_255_NON_PROPORTIONAL,
            normalized_rating_max_value=normalized_rating_max_value,
        )

        from ._id3v1_preserver import _Id3v1Preserver
        from ._id3v2_flac_handler import _Id3v2FlacHandler
        from ._id3v2_reader import _Id3v2Reader
        from ._id3v2_writer import _Id3v2Writer

        self._reader = _Id3v2Reader(self)
        self._writer = _Id3v2Writer(self)
        self._flac_handler = _Id3v2FlacHandler(self)
        self._id3v1_preserver = _Id3v1Preserver(self)

    def _extract_mutagen_metadata(self) -> RawMetadataDict:
        try:
            id3 = ID3(self.audio_file.file_path, load_v1=False, translate=False)

            # Upgrade to specified version if different
            if id3.version != self.id3v2_version:
                id3.version = self.id3v2_version

            return cast(RawMetadataDict, id3)
        except ID3NoHeaderError:
            try:
                id3 = ID3(self.audio_file.file_path, load_v1=True, translate=False)
                id3.clear()  # Exclude ID3v1 tags
                id3.version = self.id3v2_version
                return cast(RawMetadataDict, id3)
            except ID3NoHeaderError:
                # Create empty ID3 object - will be saved during write operations
                # This allows write operations to work with files that have no ID3v2 header
                id3 = ID3()
                id3.version = self.id3v2_version
                return cast(RawMetadataDict, id3)

    def _convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
        self, raw_mutagen_metadata: MutagenMetadata
    ) -> RawMetadataDict:
        return self._reader.convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(raw_mutagen_metadata)

    def _get_raw_rating_by_traktor_or_not(self, raw_clean_metadata: RawMetadataDict) -> tuple[int | None, bool]:
        for raw_metadata_key, raw_metadata_values in raw_clean_metadata.items():
            if raw_metadata_values and len(raw_metadata_values) > 0 and raw_metadata_key == self.Id3TextFrame.RATING:
                first_popm = cast(list, raw_metadata_values)
                first_popm_identifier = first_popm[0]
                first_popm_rating = first_popm[1]
                if first_popm_identifier.find("Traktor") != -1:
                    return int(first_popm_rating), True
                return int(first_popm_rating), False

        return None, False

    def _update_undirectly_mapped_metadata(
        self,
        raw_mutagen_metadata: ID3,
        app_metadata_value: UnifiedMetadataValue,
        unified_metadata_key: UnifiedMetadataKey,
    ) -> None:
        self._writer.update_undirectly_mapped_metadata(raw_mutagen_metadata, app_metadata_value, unified_metadata_key)

    def _get_undirectly_mapped_metadata_value_other_than_rating_from_raw_clean_metadata(
        self, raw_clean_metadata: RawMetadataDict, unified_metadata_key: UnifiedMetadataKey
    ) -> UnifiedMetadataValue:
        if unified_metadata_key == UnifiedMetadataKey.REPLAYGAIN:
            replaygain_key = self.Id3TextFrame.REPLAYGAIN
            if replaygain_key not in raw_clean_metadata:
                return None
            replaygain_value = raw_clean_metadata[replaygain_key]
            if replaygain_value is None:
                return None
            if len(replaygain_value) == 0:
                return None
            first_value = replaygain_value[0]
            return cast(UnifiedMetadataValue, first_value)
        if unified_metadata_key == UnifiedMetadataKey.MUSICBRAINZ_TRACKID:
            musicbrainz_trackid_key = cast(RawMetadataKey, "MUSICBRAINZ_TRACKID")
            if musicbrainz_trackid_key not in raw_clean_metadata:
                return None
            trackid_value = raw_clean_metadata[musicbrainz_trackid_key]
            if trackid_value is None:
                return None
            if len(trackid_value) == 0:
                return None
            first_value = trackid_value[0]
            return cast(UnifiedMetadataValue, first_value)
        if unified_metadata_key == UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS:
            musicbrainz_artistids_key = cast(RawMetadataKey, "MUSICBRAINZ_ARTISTIDS")
            if musicbrainz_artistids_key not in raw_clean_metadata:
                return None
            artistids_value = raw_clean_metadata[musicbrainz_artistids_key]
            if artistids_value is None:
                return None
            if len(artistids_value) == 0:
                return None
            # Use base class's smart parsing to handle separator-based values
            return self._get_value_from_multi_values_data(
                unified_metadata_key, cast(list[str], artistids_value), musicbrainz_artistids_key
            )
        if unified_metadata_key == UnifiedMetadataKey.DISC_NUMBER:
            tpos_key = self.Id3TextFrame.DISC_NUMBER
            if tpos_key not in raw_clean_metadata:
                return None
            tpos_value = raw_clean_metadata[tpos_key]
            if tpos_value is None or len(tpos_value) == 0:
                return None
            tpos_str = str(tpos_value[0])
            return parse_disc_number_from_combined_str(tpos_str)
        if unified_metadata_key == UnifiedMetadataKey.DISC_TOTAL:
            tpos_key = self.Id3TextFrame.DISC_NUMBER
            if tpos_key not in raw_clean_metadata:
                return None
            tpos_value = raw_clean_metadata[tpos_key]
            if tpos_value is None or len(tpos_value) == 0:
                return None
            tpos_str = str(tpos_value[0])
            return parse_disc_total_from_combined_str(tpos_str)
        msg = f"Metadata key not handled: {unified_metadata_key}"
        raise MetadataFieldNotSupportedByMetadataFormatError(msg)

    def _update_formatted_value_in_raw_mutagen_metadata(
        self,
        raw_mutagen_metadata: ID3,
        raw_metadata_key: RawMetadataKey,
        app_metadata_value: UnifiedMetadataValue,
    ) -> None:
        self._writer.update_formatted_value_in_raw_mutagen_metadata(
            raw_mutagen_metadata, raw_metadata_key, app_metadata_value
        )

    def _preserve_id3v1_metadata(self, file_path: str) -> bytes | None:
        return self._id3v1_preserver.preserve_id3v1_metadata(file_path)

    def _save_with_id3v1_preservation(self, file_path: str, id3v1_data: bytes | None) -> None:
        self._id3v1_preserver.save_with_id3v1_preservation(file_path, id3v1_data)

    def _save_with_version(self, file_path: str) -> None:
        self._id3v1_preserver.save_with_version(file_path)

    def update_metadata(self, unified_metadata: UnifiedMetadata) -> None:
        """Update ID3v2 metadata using hybrid approach: mutagen for most formats, external tools for FLAC.

        This method automatically chooses the appropriate tool based on the audio file format
        to ensure optimal performance and file integrity.

        Format-Specific Behavior:
        - **MP3 and other formats**: Uses mutagen (Python library) for fast, reliable updates
        - **FLAC files**: Uses external tools (id3v2/mid3v2) to prevent file corruption

        Why External Tools for FLAC?
        - Mutagen's ID3 class corrupts FLAC file structure when writing ID3v2 tags
        - External tools properly handle FLAC's metadata block structure
        - Prevents "Not a valid FLAC file" errors and file corruption

        Tool Selection Logic:
        - **ID3v2.3**: Uses 'id3v2' command-line tool
        - **ID3v2.4**: Uses 'mid3v2' command-line tool
        - **Other formats**: Uses mutagen for optimal performance

        Key Features:
        - **Version Control**: Maintains specified ID3v2 version (2.3 or 2.4)
        - **ID3v1 Preservation**: Preserves existing ID3v1 tags when present
        - **File Integrity**: Prevents corruption across all supported formats

        External Tool Requirements (FLAC only):
        - Requires 'id3v2' or 'mid3v2' command-line tools
        - Falls back to FileCorruptedError if tools are not available

        Args:
            unified_metadata: Dictionary of metadata to write/update
                             Use None values to delete specific fields

        Raises:
            MetadataFieldNotSupportedByMetadataFormatError: If field not supported
            FileCorruptedError: If external tools fail or are not found (FLAC only)
            ConfigurationError: If rating configuration is invalid
        """
        # For FLAC files, use external tools instead of mutagen to avoid file corruption
        if self.audio_file.file_extension == ".flac":
            self._update_metadata_for_flac(unified_metadata)
            return

        if not self.metadata_keys_direct_map_write:
            msg = "This format does not support metadata modification"
            raise MetadataFieldNotSupportedByMetadataFormatError(msg)

        self._validate_and_process_rating(unified_metadata)

        # Preserve ID3v1 metadata before any modifications
        id3v1_data = self._preserve_id3v1_metadata(self.audio_file.file_path)

        # Update the raw mutagen metadata (without saving yet)
        if self.raw_mutagen_metadata is None:
            self.raw_mutagen_metadata = cast(MutagenMetadata, self._extract_mutagen_metadata())

        id3_metadata: ID3 = cast(ID3, self.raw_mutagen_metadata)

        for unified_metadata_key in list(unified_metadata.keys()):
            app_metadata_value = unified_metadata[unified_metadata_key]
            if unified_metadata_key not in self.metadata_keys_direct_map_write:
                metadata_format_name = self._get_formatted_metadata_format_name()
                msg = f"{unified_metadata_key} metadata not supported by {metadata_format_name} format"
                raise MetadataFieldNotSupportedByMetadataFormatError(msg)
            raw_metadata_key = self.metadata_keys_direct_map_write[unified_metadata_key]
            if raw_metadata_key:
                self._update_formatted_value_in_raw_mutagen_metadata(
                    raw_mutagen_metadata=id3_metadata,
                    raw_metadata_key=raw_metadata_key,
                    app_metadata_value=app_metadata_value,
                )
            else:
                self._update_undirectly_mapped_metadata(
                    raw_mutagen_metadata=id3_metadata,
                    app_metadata_value=app_metadata_value,
                    unified_metadata_key=unified_metadata_key,
                )

        # Save with ID3v1 preservation
        self._save_with_id3v1_preservation(self.audio_file.file_path, id3v1_data)

    def _update_metadata_for_flac(self, unified_metadata: UnifiedMetadata) -> None:
        self._flac_handler.update_metadata_for_flac(unified_metadata)

    def delete_metadata(self) -> bool:
        """Delete all ID3v2 metadata from the audio file.

        This removes all ID3v2 frames from the file while preserving the audio data.
        Uses ID3.delete() which is more reliable than deleting individual frames,
        especially for non-MP3 files like FLAC that might have ID3v2 tags.

        Returns:
            bool: True if metadata was successfully deleted, False otherwise
        """
        try:
            # Create a new ID3 instance and use delete() to remove all ID3v2 tags
            id3 = ID3(self.audio_file.file_path)
            id3.delete()
        except ID3NoHeaderError:
            # No ID3 tags present, consider this a success
            return True
        except Exception:
            return False
        else:
            return True

    def get_header_info(self) -> dict:
        try:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = cast(MutagenMetadata, self._extract_mutagen_metadata())

            if not self.raw_mutagen_metadata:
                return {"present": False, "version": None, "header_size_bytes": 0, "flags": {}, "extended_header": {}}

            id3_metadata: ID3 = cast(ID3, self.raw_mutagen_metadata)

            # Get ID3v2 version
            version = getattr(id3_metadata, "version", None)
            version_str = f"{version[0]}.{version[1]}.{version[2]}" if version else None

            # Get header size
            header_size = getattr(id3_metadata, "size", 0)

            # Get flags
            flags = {}
            if hasattr(id3_metadata, "flags"):
                flags = {
                    "unsync": bool(id3_metadata.flags & 0x80),
                    "extended_header": bool(id3_metadata.flags & 0x40),
                    "experimental": bool(id3_metadata.flags & 0x20),
                    "footer": bool(id3_metadata.flags & 0x10),
                }

            # Get extended header info
            extended_header = {}
            if hasattr(id3_metadata, "extended_header"):
                ext_header = id3_metadata.extended_header
                if ext_header:
                    extended_header = {
                        "size": getattr(ext_header, "size", 0),
                        "flags": getattr(ext_header, "flags", 0),
                        "padding_size": getattr(ext_header, "padding_size", 0),
                    }
        except Exception:
            return {"present": False, "version": None, "header_size_bytes": 0, "flags": {}, "extended_header": {}}
        else:
            return {
                "present": True,
                "version": version_str,
                "header_size_bytes": header_size,
                "flags": flags,
                "extended_header": extended_header,
            }

    def get_raw_metadata_info(self) -> dict:
        try:
            if self.raw_mutagen_metadata is None:
                self.raw_mutagen_metadata = cast(MutagenMetadata, self._extract_mutagen_metadata())

            if not self.raw_mutagen_metadata:
                return {"raw_data": None, "parsed_fields": {}, "frames": {}, "comments": {}, "chunk_structure": {}}

            id3_metadata: ID3 = cast(ID3, self.raw_mutagen_metadata)

            frames = {}
            for frame_id, frame in id3_metadata.items():
                frames[frame_id] = {
                    "text": str(frame) if hasattr(frame, "__str__") else repr(frame),
                    "size": getattr(frame, "size", 0),
                    "flags": getattr(frame, "flags", 0),
                }
        except Exception:
            return {"raw_data": None, "parsed_fields": {}, "frames": {}, "comments": {}, "chunk_structure": {}}
        else:
            return {
                "raw_data": None,  # ID3v2 data is complex, not storing raw bytes
                "parsed_fields": {},
                "frames": frames,
                "comments": {},
                "chunk_structure": {},
            }

    def sanitize_raw_metadata_for_display(self, raw_info: dict) -> dict:
        return sanitize_id3v2_raw_info(raw_info)
