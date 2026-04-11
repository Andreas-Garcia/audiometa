"""ID3v2 writer helper for updating metadata in ID3v2 format."""

from typing import TYPE_CHECKING, Any

from mutagen.id3 import ID3
from mutagen.id3._frames import TPOS, TXXX, UFID

from audiometa.manager._MetadataManager import _MetadataManager as MetadataManager
from audiometa.utils.disc_number_read import parse_disc_number_from_combined_str, parse_disc_total_from_combined_str
from audiometa.utils.types import RawMetadataKey, UnifiedMetadataValue
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

if TYPE_CHECKING:
    from ._Id3v2Manager import _Id3v2Manager

from ._id3v2_constants import ID3V2_VERSION_3, ID3V2_VERSION_4


class _Id3v2Writer:
    """Helper class for writing ID3v2 metadata."""

    def __init__(self, manager: "_Id3v2Manager"):
        """Initialize writer with reference to manager.

        Args:
            manager: The ID3v2 manager instance
        """
        self.manager = manager

    def update_undirectly_mapped_metadata(
        self,
        raw_mutagen_metadata: ID3,
        app_metadata_value: UnifiedMetadataValue,
        unified_metadata_key: UnifiedMetadataKey,
    ) -> None:
        """Update indirectly mapped metadata fields.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            app_metadata_value: Application metadata value to write
            unified_metadata_key: Unified metadata key
        """
        if unified_metadata_key == UnifiedMetadataKey.REPLAYGAIN:
            self._write_replaygain(raw_mutagen_metadata, app_metadata_value)
        elif unified_metadata_key == UnifiedMetadataKey.MUSICBRAINZ_TRACKID:
            self._write_musicbrainz_trackid(raw_mutagen_metadata, app_metadata_value)
        elif unified_metadata_key == UnifiedMetadataKey.MUSICBRAINZ_ARTISTIDS:
            self._write_musicbrainz_artistids(raw_mutagen_metadata, app_metadata_value)
        elif unified_metadata_key in (UnifiedMetadataKey.DISC_NUMBER, UnifiedMetadataKey.DISC_TOTAL):
            self._write_disc_number_or_total(raw_mutagen_metadata, app_metadata_value, unified_metadata_key)

    def update_formatted_value_in_raw_mutagen_metadata(
        self,
        raw_mutagen_metadata: ID3,
        raw_metadata_key: RawMetadataKey,
        app_metadata_value: UnifiedMetadataValue,
    ) -> None:
        """Update formatted value in raw mutagen metadata.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            raw_metadata_key: Raw metadata key
            app_metadata_value: Application metadata value to write
        """
        raw_mutagen_metadata_id3: ID3 = raw_mutagen_metadata
        raw_mutagen_metadata_id3.delall(raw_metadata_key)

        # If value is None, don't add any frames (field is removed)
        if app_metadata_value is None:
            return

        # Defensive check: if list contains None values, filter them out (should not happen after base class filtering)
        if isinstance(app_metadata_value, list):
            app_metadata_value = [v for v in app_metadata_value if v is not None and v != ""]
            if not app_metadata_value:
                return

        # Handle multiple values by creating separate frames for multi-value fields
        if isinstance(app_metadata_value, list) and all(isinstance(item, str) for item in app_metadata_value):
            # Get the corresponding UnifiedMetadataKey
            unified_metadata_key = None
            if self.manager.metadata_keys_direct_map_write is None:
                return
            for key, raw_key in self.manager.metadata_keys_direct_map_write.items():
                if raw_key == raw_metadata_key:
                    unified_metadata_key = key
                    break

            if unified_metadata_key and unified_metadata_key.can_semantically_have_multiple_values():
                # Check ID3v2 version to determine handling
                # Use self.id3v2_version instead of trying to get it from the mutagen object
                # as the object might not have the version set yet during writing
                id3v2_version = self.manager.id3v2_version

                # ID3v2.4 supports multi-value text frames (single frame with null-separated values per spec)
                if id3v2_version[1] >= ID3V2_VERSION_4:
                    # Create single frame with multiple text values (ID3v2.4 spec: null-separated values in one frame)
                    # Officially supported fields: TPE1 (artists), TPE2 (album artists), TCOM (composers), TCON (genres)
                    text_frame_class = self.manager.ID3_TEXT_FRAME_CLASS_MAP[raw_metadata_key]
                    # Values are already filtered at the base level
                    if app_metadata_value:
                        self._add_id3_frame_v24_multi(raw_mutagen_metadata_id3, text_frame_class, app_metadata_value)
                    return

                # For ID3v2.3, use concatenation with separators (ID3v2.3 doesn't support null-separated values)
                # Find a separator that doesn't appear in any of the values and concatenate
                separator = MetadataManager.find_safe_separator(app_metadata_value)
                app_metadata_value = separator.join(app_metadata_value)
                # Continue to handle as single value
            else:
                # For non-multi-value fields, concatenate with separators as fallback
                # Find a separator that doesn't appear in any of the values and concatenate
                separator = MetadataManager.find_safe_separator(app_metadata_value)
                app_metadata_value = separator.join(app_metadata_value)

        # Handle single values
        text_frame_class = self.manager.ID3_TEXT_FRAME_CLASS_MAP[raw_metadata_key]
        self._add_id3_frame(raw_mutagen_metadata_id3, text_frame_class, raw_metadata_key, app_metadata_value)

    def _add_id3_frame(
        self,
        raw_mutagen_metadata_id3: ID3,
        text_frame_class: type[Any],
        raw_metadata_key: RawMetadataKey,
        app_metadata_value: UnifiedMetadataValue,
    ) -> None:
        """Add a single ID3 frame with proper encoding and format handling.

        Args:
            raw_mutagen_metadata_id3: Raw mutagen ID3 metadata object
            text_frame_class: Text frame class to use
            raw_metadata_key: Raw metadata key
            app_metadata_value: Application metadata value to write
        """
        # Determine encoding based on ID3v2 version
        encoding = 0 if self.manager.id3v2_version[1] == ID3V2_VERSION_3 else 3

        if raw_metadata_key == self.manager.Id3TextFrame.RATING:
            raw_mutagen_metadata_id3.add(
                text_frame_class(email=self.manager.ID3_RATING_APP_EMAIL, rating=app_metadata_value)
            )
        elif raw_metadata_key == self.manager.Id3TextFrame.COMMENT:
            # Handle COMM frames (comment frames)
            raw_mutagen_metadata_id3.add(
                text_frame_class(encoding=encoding, lang="eng", desc="", text=app_metadata_value)
            )
        elif raw_metadata_key == self.manager.Id3TextFrame.UNSYNCHRONIZED_LYRICS:
            # Handle USLT frames (unsynchronized lyrics frames)
            raw_mutagen_metadata_id3.add(
                text_frame_class(encoding=encoding, lang="eng", desc="", text=app_metadata_value)
            )
        elif raw_metadata_key == self.manager.Id3TextFrame.URL:
            # Handle WOAR frames (official artist/performer webpage)
            raw_mutagen_metadata_id3.add(text_frame_class(url=app_metadata_value))
        elif raw_metadata_key == self.manager.Id3TextFrame.BPM:
            # Handle TBPM frames (BPM must be a string)
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=encoding, text=str(app_metadata_value)))
        elif raw_metadata_key == self.manager.Id3TextFrame.TRACK_NUMBER:
            # Handle TRCK frames (track number must be a string)
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=encoding, text=str(app_metadata_value)))
        else:
            raw_mutagen_metadata_id3.add(text_frame_class(encoding=encoding, text=app_metadata_value))

    def _add_id3_frame_v24_multi(
        self, raw_mutagen_metadata_id3: ID3, text_frame_class: type[Any], values: list[str]
    ) -> None:
        """ID3v2.4: add a single text frame containing multiple null-separated values.

        Mutagen accepts a list for the `text` parameter and will write it as
        null-separated strings in a single frame which matches the ID3v2.4 spec.

        Args:
            raw_mutagen_metadata_id3: Raw mutagen ID3 metadata object
            text_frame_class: Text frame class to use
            values: List of string values to write
        """
        # Add one frame with multiple text values (mutagen handles null separation)
        raw_mutagen_metadata_id3.add(text_frame_class(encoding=3, text=values))

    def _write_replaygain(self, raw_mutagen_metadata: ID3, app_metadata_value: UnifiedMetadataValue) -> None:
        """Write ReplayGain metadata.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            app_metadata_value: ReplayGain value to write
        """
        # Remove existing TXXX:REPLAYGAIN frames
        raw_mutagen_metadata.delall("TXXX:REPLAYGAIN")
        if app_metadata_value is not None:
            # Add new TXXX frame with desc 'REPLAYGAIN'
            raw_mutagen_metadata.add(TXXX(encoding=3, desc="REPLAYGAIN", text=str(app_metadata_value)))

    def _write_musicbrainz_trackid(self, raw_mutagen_metadata: ID3, app_metadata_value: UnifiedMetadataValue) -> None:
        """Write MusicBrainz Track ID metadata.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            app_metadata_value: MusicBrainz Track ID value to write
        """
        # Remove existing UFID frames with MusicBrainz owner
        raw_mutagen_metadata.delall("UFID:http://musicbrainz.org")
        # Remove existing TXXX frames with MusicBrainz Track Id description
        raw_mutagen_metadata.delall("TXXX:MusicBrainz Track Id")

        if app_metadata_value is not None and app_metadata_value != "":
            # Normalize UUID: convert 32-char hex to 36-char hyphenated format if needed
            track_id = str(app_metadata_value).strip()
            uuid_hex_length = 32
            if len(track_id) == uuid_hex_length and all(c in "0123456789abcdefABCDEF" for c in track_id):
                track_id = f"{track_id[:8]}-{track_id[8:12]}-{track_id[12:16]}-{track_id[16:20]}-{track_id[20:32]}"

            # Write as UFID frame with owner "http://musicbrainz.org"
            # UFID data should be the UUID as bytes (without null terminator)
            track_id_bytes = track_id.encode("utf-8")
            raw_mutagen_metadata.add(UFID(owner="http://musicbrainz.org", data=track_id_bytes))

    def _write_musicbrainz_artistids(self, raw_mutagen_metadata: ID3, app_metadata_value: UnifiedMetadataValue) -> None:
        """Write MusicBrainz Artist IDs metadata.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            app_metadata_value: MusicBrainz Artist IDs value to write (list of UUIDs)
        """
        # Remove existing TXXX frames with MusicBrainz Artist Id description (case-insensitive)
        # We need to check all TXXX frames and remove matching ones
        frames_to_remove = []
        for frame_id, frame in raw_mutagen_metadata.items():
            if (
                frame_id.startswith("TXXX")
                and hasattr(frame, "desc")
                and str(frame.desc).lower() == "musicbrainz artist id"
            ):
                frames_to_remove.append(frame_id)
        for frame_id in frames_to_remove:
            raw_mutagen_metadata.delall(frame_id)

        if app_metadata_value is not None and isinstance(app_metadata_value, list) and len(app_metadata_value) > 0:
            # Normalize UUIDs: convert 32-char hex to 36-char hyphenated format if needed
            normalized_ids = []
            for artist_id in app_metadata_value:
                if artist_id and artist_id.strip():
                    normalized_id = str(artist_id).strip()
                    uuid_hex_length = 32
                    if len(normalized_id) == uuid_hex_length and all(
                        c in "0123456789abcdefABCDEF" for c in normalized_id
                    ):
                        normalized_id = (
                            f"{normalized_id[:8]}-{normalized_id[8:12]}-"
                            f"{normalized_id[12:16]}-{normalized_id[16:20]}-{normalized_id[20:32]}"
                        )
                    normalized_ids.append(normalized_id)

            if normalized_ids:
                encoding = 0 if self.manager.id3v2_version[1] == ID3V2_VERSION_3 else 3

                # For ID3v2.4, use null-separated values (per ID3v2.4 spec)
                if self.manager.id3v2_version[1] >= ID3V2_VERSION_4:
                    # Join with null byte separator
                    text_value = "\x00".join(normalized_ids)
                    raw_mutagen_metadata.add(TXXX(encoding=encoding, desc="MusicBrainz Artist Id", text=text_value))
                else:
                    # For ID3v2.3, use separator-based concatenation
                    separator = MetadataManager.find_safe_separator(normalized_ids)
                    text_value = separator.join(normalized_ids)
                    raw_mutagen_metadata.add(TXXX(encoding=encoding, desc="MusicBrainz Artist Id", text=text_value))

    def _write_disc_number_or_total(
        self,
        raw_mutagen_metadata: ID3,
        app_metadata_value: UnifiedMetadataValue,
        unified_metadata_key: UnifiedMetadataKey,
    ) -> None:
        """Write disc number or disc total metadata.

        Args:
            raw_mutagen_metadata: Raw mutagen ID3 metadata object
            app_metadata_value: Disc number or total value to write
            unified_metadata_key: Unified metadata key (DISC_NUMBER or DISC_TOTAL)
        """
        tpos_key = self.manager.Id3TextFrame.DISC_NUMBER
        tpos_frame_class = TPOS
        encoding = 0 if self.manager.id3v2_version[1] == ID3V2_VERSION_3 else 3

        if unified_metadata_key == UnifiedMetadataKey.DISC_NUMBER:
            current_tpos = raw_mutagen_metadata.get(tpos_key)
            current_total = None
            if current_tpos and len(current_tpos.text) > 0:
                tpos_str = str(current_tpos.text[0])
                current_total = parse_disc_total_from_combined_str(tpos_str)

            raw_mutagen_metadata.delall(tpos_key)
            if app_metadata_value is not None:
                if not isinstance(app_metadata_value, int):
                    msg = f"DISC_NUMBER must be an integer, got {type(app_metadata_value).__name__}"
                    raise TypeError(msg)
                disc_number = min(255, max(0, app_metadata_value))
                tpos_value = f"{disc_number}/{current_total}" if current_total is not None else str(disc_number)
                raw_mutagen_metadata.add(tpos_frame_class(encoding=encoding, text=tpos_value))
        elif unified_metadata_key == UnifiedMetadataKey.DISC_TOTAL:
            current_tpos = raw_mutagen_metadata.get(tpos_key)
            current_disc_number = None
            if current_tpos and len(current_tpos.text) > 0:
                tpos_str = str(current_tpos.text[0])
                current_disc_number = parse_disc_number_from_combined_str(tpos_str)

            raw_mutagen_metadata.delall(tpos_key)
            if app_metadata_value is not None:
                if not isinstance(app_metadata_value, int):
                    msg = f"DISC_TOTAL must be an integer, got {type(app_metadata_value).__name__}"
                    raise TypeError(msg)
                disc_total = min(255, max(0, app_metadata_value))
                if current_disc_number is not None:
                    tpos_value = f"{current_disc_number}/{disc_total}"
                    raw_mutagen_metadata.add(tpos_frame_class(encoding=encoding, text=tpos_value))
                else:
                    msg = "Cannot set DISC_TOTAL without DISC_NUMBER"
                    raise ValueError(msg)
            elif current_disc_number is not None:
                tpos_value = str(current_disc_number)
                raw_mutagen_metadata.add(tpos_frame_class(encoding=encoding, text=tpos_value))
