"""ID3v2 reader helper for converting raw mutagen metadata to unified format."""

from typing import TYPE_CHECKING, cast

from mutagen._file import FileType as MutagenMetadata
from mutagen.id3 import ID3

from audiometa.utils.types import RawMetadataDict, RawMetadataKey

if TYPE_CHECKING:
    from ._Id3v2Manager import _Id3v2Manager

from ._id3v2_constants import ID3V2_DATE_FORMAT_LENGTH


class _Id3v2Reader:
    """Helper class for reading and converting ID3v2 metadata."""

    def __init__(self, manager: "_Id3v2Manager"):
        """Initialize reader with reference to manager.

        Args:
            manager: The ID3v2 manager instance
        """
        self.manager = manager

    def convert_raw_mutagen_metadata_to_dict_with_potential_duplicate_keys(
        self, raw_mutagen_metadata: MutagenMetadata, result: RawMetadataDict | None = None
    ) -> RawMetadataDict:
        """Convert raw mutagen metadata to dictionary with potential duplicate keys.

        Args:
            raw_mutagen_metadata: Raw mutagen metadata object
            result: Optional existing result dictionary to merge into

        Returns:
            Dictionary of raw metadata with potential duplicate keys
        """
        if result is None:
            result = {}

        for frame_key in self.manager.Id3TextFrame.__members__.values():
            if frame_key == self.manager.Id3TextFrame.RATING:
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    popm_key = raw_mutagen_frame[0]
                    if popm_key.startswith(self.manager.Id3TextFrame.RATING):
                        from mutagen.id3._frames import POPM

                        popm: POPM = raw_mutagen_frame[1]
                        popm_key_without_prefixes = popm_key.replace(f"{self.manager.Id3TextFrame.RATING}:", "")
                        result[self.manager.Id3TextFrame.RATING] = [
                            popm_key_without_prefixes,
                            getattr(popm, "rating", 0),
                        ]
                        break
            elif frame_key == self.manager.Id3TextFrame.COMMENT:
                # Handle COMM frames (comment frames)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith("COMM"):
                        comm_frame = raw_mutagen_frame[1]
                        result[frame_key] = comm_frame.text
                        break
            elif frame_key == self.manager.Id3TextFrame.UNSYNCHRONIZED_LYRICS:
                # Handle USLT frames (unsynchronized lyrics frames)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith("USLT"):
                        uslt_frame = raw_mutagen_frame[1]
                        result[frame_key] = [uslt_frame.text]
                        break
            elif frame_key == self.manager.Id3TextFrame.URL:
                # Handle WOAR frames (official artist/performer webpage)
                for raw_mutagen_frame in raw_mutagen_metadata.items():
                    if raw_mutagen_frame[0].startswith("WOAR"):
                        woar_frame = raw_mutagen_frame[1]
                        result[frame_key] = [woar_frame.url]
                        break
            else:
                raw_metadata_id3: ID3 = cast(ID3, raw_mutagen_metadata)
                frame_value = frame_key in raw_metadata_id3 and raw_metadata_id3[frame_key]
                if not frame_value:
                    continue

                if not frame_value.text:
                    continue

                result[frame_key] = frame_value.text

        # Handle TXXX frames for REPLAYGAIN
        for raw_mutagen_frame in raw_mutagen_metadata.items():
            if raw_mutagen_frame[0].startswith("TXXX"):
                txxx_frame = raw_mutagen_frame[1]
                if hasattr(txxx_frame, "desc") and txxx_frame.desc == "REPLAYGAIN":
                    result[self.manager.Id3TextFrame.REPLAYGAIN] = txxx_frame.text
                    break

        # Handle UFID frames for MusicBrainz Track ID (preferred)
        musicbrainz_trackid = self._read_musicbrainz_trackid_from_ufid(raw_mutagen_metadata)

        # Handle TXXX frames for MusicBrainz Track ID (fallback)
        if not musicbrainz_trackid:
            musicbrainz_trackid = self._read_musicbrainz_trackid_from_txxx(raw_mutagen_metadata)

        if musicbrainz_trackid:
            # Use a special key for MusicBrainz Track ID (not a text frame, so use string key)
            result[cast(RawMetadataKey, "MUSICBRAINZ_TRACKID")] = [musicbrainz_trackid]

        # Handle TXXX frames for MusicBrainz Artist ID
        musicbrainz_artistids = self._read_musicbrainz_artistids_from_txxx(raw_mutagen_metadata)
        if musicbrainz_artistids:
            # Use a special key for MusicBrainz Artist IDs (not a text frame, so use string key)
            # Base class will handle separator parsing via _get_value_from_multi_values_data
            result[cast(RawMetadataKey, "MUSICBRAINZ_ARTISTIDS")] = musicbrainz_artistids

        # Special handling for release date: if TDRC is not present, try to construct from TYER + TDAT
        self._construct_release_date_from_year_and_date(result)

        return result

    def _read_musicbrainz_trackid_from_ufid(self, raw_mutagen_metadata: MutagenMetadata) -> str | None:
        """Read MusicBrainz Track ID from UFID frames.

        Args:
            raw_mutagen_metadata: Raw mutagen metadata object

        Returns:
            MusicBrainz Track ID as string, or None if not found
        """
        for raw_mutagen_frame in raw_mutagen_metadata.items():
            if raw_mutagen_frame[0].startswith("UFID"):
                ufid_frame = raw_mutagen_frame[1]
                if (
                    hasattr(ufid_frame, "owner")
                    and ufid_frame.owner == "http://musicbrainz.org"
                    and hasattr(ufid_frame, "data")
                ):
                    # UFID data is bytes, decode to string
                    try:
                        musicbrainz_trackid = ufid_frame.data.decode("utf-8", errors="replace").strip("\x00")
                        # Normalize to hyphenated UUID format if it's 32 hex chars
                        return self._normalize_uuid(musicbrainz_trackid)
                    except (UnicodeDecodeError, AttributeError):
                        pass
        return None

    def _read_txxx_frame_text(
        self, raw_mutagen_metadata: MutagenMetadata, description: str, case_sensitive: bool = True
    ) -> str | None:
        """Read text value from TXXX frame with matching description.

        Args:
            raw_mutagen_metadata: Raw mutagen metadata object
            description: Description to match
            case_sensitive: Whether description matching is case-sensitive

        Returns:
            Text value as string, or None if not found
        """
        for raw_mutagen_frame in raw_mutagen_metadata.items():
            if raw_mutagen_frame[0].startswith("TXXX"):
                txxx_frame = raw_mutagen_frame[1]
                if not hasattr(txxx_frame, "desc") or not txxx_frame.text:
                    continue

                desc_match = (
                    txxx_frame.desc == description
                    if case_sensitive
                    else str(txxx_frame.desc).lower() == description.lower()
                )
                if desc_match:
                    return txxx_frame.text[0] if isinstance(txxx_frame.text, list) else str(txxx_frame.text)
        return None

    def _read_musicbrainz_trackid_from_txxx(self, raw_mutagen_metadata: MutagenMetadata) -> str | None:
        """Read MusicBrainz Track ID from TXXX frames (fallback).

        Args:
            raw_mutagen_metadata: Raw mutagen metadata object

        Returns:
            MusicBrainz Track ID as string, or None if not found
        """
        text_value = self._read_txxx_frame_text(raw_mutagen_metadata, "MusicBrainz Track Id", case_sensitive=True)
        if text_value:
            return self._normalize_uuid(text_value)
        return None

    def _read_musicbrainz_artistids_from_txxx(self, raw_mutagen_metadata: MutagenMetadata) -> list[str]:
        """Read MusicBrainz Artist IDs from TXXX frames.

        Args:
            raw_mutagen_metadata: Raw mutagen metadata object

        Returns:
            List of MusicBrainz Artist IDs (may contain separator-based values)
        """
        # Get the TXXX frame directly to handle both list and string values
        for raw_mutagen_frame in raw_mutagen_metadata.items():
            if raw_mutagen_frame[0].startswith("TXXX"):
                txxx_frame = raw_mutagen_frame[1]
                if not hasattr(txxx_frame, "desc") or not txxx_frame.text:
                    continue

                desc_match = str(txxx_frame.desc).lower() == "musicbrainz artist id"
                if desc_match:
                    # Handle both list and string values from mutagen
                    if isinstance(txxx_frame.text, list):
                        # Mutagen already split the values
                        return [str(val) for val in txxx_frame.text if val]
                    # Single string value - may contain null-separated values (ID3v2.4)
                    text_str = str(txxx_frame.text)
                    if "\x00" in text_str:
                        # Split by null bytes (ID3v2.4 format)
                        return [val for val in text_str.split("\x00") if val]
                    # Single value or separator-based (ID3v2.3)
                    return [text_str]
        return []

    def _construct_release_date_from_year_and_date(self, result: RawMetadataDict) -> None:
        """Construct release date from TYER + TDAT if TDRC is not present.

        Args:
            result: Raw metadata dictionary to update
        """
        # Special handling for release date: if TDRC is not present, try to construct from TYER + TDAT
        # Only do this for ID3v2 files (not ID3v1) and only when both TYER and TDAT are present
        if self.manager.Id3TextFrame.RECORDING_TIME not in result:
            year_key: RawMetadataKey = self.manager.Id3TextFrame.YEAR
            date_key: RawMetadataKey = self.manager.Id3TextFrame.DATE
            tyer_value = result.get(year_key, None)
            tdat_value = result.get(date_key, None)
            if tyer_value and tdat_value:
                # Parse TDAT (DDMM) and TYER to construct YYYY-MM-DD
                try:
                    year = str(tyer_value[0]) if isinstance(tyer_value, list) else str(tyer_value)
                    date_str = str(tdat_value[0]) if isinstance(tdat_value, list) else str(tdat_value)
                    if len(date_str) == ID3V2_DATE_FORMAT_LENGTH:  # DDMM format
                        day = date_str[:2]
                        month = date_str[2:]
                        # Construct YYYY-MM-DD
                        release_date = f"{year}-{month}-{day}"
                        result[self.manager.Id3TextFrame.RECORDING_TIME] = [release_date]
                except (IndexError, ValueError):
                    pass  # If parsing fails, don't add release date

    @staticmethod
    def _normalize_uuid(uuid_str: str) -> str:
        """Normalize UUID from 32-char hex to 36-char hyphenated format if needed.

        Args:
            uuid_str: UUID string (may be 32-char hex or 36-char hyphenated)

        Returns:
            Normalized UUID in hyphenated format
        """
        uuid_hex_length = 32
        if len(uuid_str) == uuid_hex_length and all(c in "0123456789abcdefABCDEF" for c in uuid_str):
            return f"{uuid_str[:8]}-{uuid_str[8:12]}-" f"{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:32]}"
        return uuid_str
