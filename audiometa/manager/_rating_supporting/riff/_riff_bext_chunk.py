"""BEXT chunk operations for RIFF/BWF files.

This module handles reading and writing of BWF (Broadcast Wave Format) bext chunks,
which contain metadata fields like Description, Originator, and loudness information.
"""

from collections.abc import Callable
from typing import Any

from ._riff_constants import (
    BEXT_LOUDNESS_METADATA_SIZE,
    BEXT_MIN_CHUNK_SIZE,
    BEXT_ORIGINATION_DATE_SIZE,
    BEXT_ORIGINATION_TIME_SIZE,
    BWF_V2_VERSION,
    RIFF_CHUNK_ID_SIZE,
    RIFF_HEADER_SIZE,
    RIFF_WAVE_FORMAT_POSITION,
)


def extract_bext_chunk(file_data: bytes, skip_id3v2_tags_func: Callable[[bytes], bytes]) -> dict[str, Any] | None:
    """Extract and parse the bext chunk from BWF files.

    BWF has multiple versions:
    - Version 0 (1997): Original specification, no UMID field
    - Version 1 (2001): Added UMID field (64 bytes)
    - Version 2 (2011): Added loudness metadata fields

    The bext chunk structure (v1):
    - Description (256 bytes, ASCII, null-terminated)
    - Originator (32 bytes, ASCII, null-terminated)
    - OriginatorReference (32 bytes, ASCII, null-terminated)
    - OriginationDate (10 bytes, ASCII, YYYY-MM-DD)
    - OriginationTime (8 bytes, ASCII, HH:MM:SS)
    - TimeReference (8 bytes, uint64, little-endian)
    - Version (2 bytes, uint16, little-endian): 0x0000 (v0), 0x0001 (v1), 0x0002 (v2)
    - UMID (64 bytes, binary, v1+ only)
    - Reserved (190 bytes, zeros)
    - CodingHistory (variable length, ASCII, null-terminated)

    BWF v2 adds loudness metadata fields (10 bytes total) at the START of reserved bytes (offset 412):
    - LoudnessValue (2 bytes, int16, little-endian, stored as 0.01 LU units by bwfmetaedit)
    - LoudnessRange (2 bytes, int16, little-endian, stored as 0.01 LU units)
    - MaxTruePeakLevel (2 bytes, int16, little-endian, stored as 0.01 dB units)
    - MaxMomentaryLoudness (2 bytes, int16, little-endian, stored as 0.01 LU units)
    - MaxShortTermLoudness (2 bytes, int16, little-endian, stored as 0.01 LU units)
    Note: bwfmetaedit stores loudness values as 0.01 units (centi-units), so values are divided by 100.

    Args:
        file_data: Full file data (may include ID3v2 tags)
        skip_id3v2_tags_func: Function to skip ID3v2 tags from file data

    Returns:
        Dictionary with parsed bext fields or None if bext chunk not found
    """
    # Skip ID3v2 if present
    file_data = skip_id3v2_tags_func(file_data)

    # Validate RIFF header
    if (
        len(file_data) < RIFF_HEADER_SIZE
        or file_data[:RIFF_CHUNK_ID_SIZE] != b"RIFF"
        or file_data[RIFF_WAVE_FORMAT_POSITION:RIFF_HEADER_SIZE] != b"WAVE"
    ):
        return None

    pos = 12  # Start after RIFF header
    while pos < len(file_data) - 8:
        chunk_id = file_data[pos : pos + 4]
        chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")

        if chunk_id == b"bext":
            # Found bext chunk
            bext_data_start = pos + 8
            bext_data_end = bext_data_start + chunk_size

            if bext_data_end > len(file_data):
                return None

            bext_data = file_data[bext_data_start:bext_data_end]

            # Minimum bext chunk size is 602 bytes (256+32+32+10+8+8+2+64+190)
            if len(bext_data) < BEXT_MIN_CHUNK_SIZE:
                return None

            bext_fields: dict[str, Any] = {}

            # Parse fixed fields
            offset = 0

            # Description (256 bytes)
            description_bytes = bext_data[offset : offset + 256]
            description = description_bytes.split(b"\x00")[0].decode("ascii", errors="ignore").strip()
            if description:
                bext_fields["Description"] = description
            offset += 256

            # Originator (32 bytes)
            originator_bytes = bext_data[offset : offset + 32]
            originator = originator_bytes.split(b"\x00")[0].decode("ascii", errors="ignore").strip()
            if originator:
                bext_fields["Originator"] = originator
            offset += 32

            # OriginatorReference (32 bytes)
            originator_ref_bytes = bext_data[offset : offset + 32]
            originator_ref = originator_ref_bytes.split(b"\x00")[0].decode("ascii", errors="ignore").strip()
            if originator_ref:
                bext_fields["OriginatorReference"] = originator_ref
            offset += 32

            # OriginationDate (10 bytes, YYYY-MM-DD)
            origination_date_bytes = bext_data[offset : offset + BEXT_ORIGINATION_DATE_SIZE]
            origination_date = origination_date_bytes.decode("ascii", errors="ignore").strip()
            if origination_date and len(origination_date) == BEXT_ORIGINATION_DATE_SIZE:
                bext_fields["OriginationDate"] = origination_date
            offset += BEXT_ORIGINATION_DATE_SIZE

            # OriginationTime (8 bytes, HH:MM:SS)
            origination_time_bytes = bext_data[offset : offset + BEXT_ORIGINATION_TIME_SIZE]
            origination_time = origination_time_bytes.decode("ascii", errors="ignore").strip()
            if origination_time and len(origination_time) == BEXT_ORIGINATION_TIME_SIZE:
                bext_fields["OriginationTime"] = origination_time
            offset += BEXT_ORIGINATION_TIME_SIZE

            # TimeReference (8 bytes, uint64, little-endian)
            if offset + 8 <= len(bext_data):
                time_reference = int.from_bytes(bext_data[offset : offset + 8], "little")
                bext_fields["TimeReference"] = time_reference
            offset += 8

            # Version (2 bytes, uint16, little-endian)
            if offset + 2 <= len(bext_data):
                version = int.from_bytes(bext_data[offset : offset + 2], "little")
                bext_fields["Version"] = version
            offset += 2

            # UMID (64 bytes, binary)
            if offset + 64 <= len(bext_data):
                umid_bytes = bext_data[offset : offset + 64]
                # Check if UMID is not all zeros
                if any(umid_bytes):
                    # Format as hex string for readability
                    umid_hex = umid_bytes.hex().upper()
                    bext_fields["UMID"] = umid_hex
            offset += 64

            # Reserved (190 bytes) - in BWF v2, loudness metadata is stored at the START of reserved bytes
            # Parse loudness metadata if BWF v2 (version >= 2)
            if version >= BWF_V2_VERSION and offset + BEXT_LOUDNESS_METADATA_SIZE <= len(bext_data):
                # Loudness metadata starts at offset 412 (start of reserved bytes area)
                # LoudnessValue (2 bytes, int16, little-endian, stored as 0.01 LU units by bwfmetaedit)
                loudness_value_raw = int.from_bytes(bext_data[offset : offset + 2], "little", signed=True)
                if loudness_value_raw != 0:  # 0 means not set
                    # bwfmetaedit stores as 0.01 units, convert to LU
                    bext_fields["LoudnessValue"] = round(loudness_value_raw / 100.0, 2)
                offset += 2

                # LoudnessRange (2 bytes, int16, little-endian, stored as 0.01 LU units)
                if offset + 2 <= len(bext_data):
                    loudness_range_raw = int.from_bytes(bext_data[offset : offset + 2], "little", signed=True)
                    if loudness_range_raw != 0:  # 0 means not set
                        bext_fields["LoudnessRange"] = round(loudness_range_raw / 100.0, 2)
                    offset += 2

                # MaxTruePeakLevel (2 bytes, int16, little-endian, stored as 0.01 dB units)
                if offset + 2 <= len(bext_data):
                    max_true_peak_raw = int.from_bytes(bext_data[offset : offset + 2], "little", signed=True)
                    if max_true_peak_raw != 0:  # 0 means not set
                        bext_fields["MaxTruePeakLevel"] = round(max_true_peak_raw / 100.0, 2)
                    offset += 2

                # MaxMomentaryLoudness (2 bytes, int16, little-endian, stored as 0.01 LU units)
                if offset + 2 <= len(bext_data):
                    max_momentary_raw = int.from_bytes(bext_data[offset : offset + 2], "little", signed=True)
                    if max_momentary_raw != 0:  # 0 means not set
                        bext_fields["MaxMomentaryLoudness"] = round(max_momentary_raw / 100.0, 2)
                    offset += 2

                # MaxShortTermLoudness (2 bytes, int16, little-endian, stored as 0.01 LU units)
                if offset + 2 <= len(bext_data):
                    max_short_term_raw = int.from_bytes(bext_data[offset : offset + 2], "little", signed=True)
                    if max_short_term_raw != 0:  # 0 means not set
                        bext_fields["MaxShortTermLoudness"] = round(max_short_term_raw / 100.0, 2)
                    offset += 2

                # Skip remaining reserved bytes (190 - 10 = 180 bytes)
                offset += 180
            else:
                # Skip all reserved bytes if not v2
                offset += 190

            # CodingHistory (variable length, null-terminated)
            if offset < len(bext_data):
                coding_history_bytes = bext_data[offset:]
                # Find null terminator or end of chunk
                null_pos = coding_history_bytes.find(b"\x00")
                if null_pos >= 0:
                    coding_history_bytes = coding_history_bytes[:null_pos]
                coding_history = coding_history_bytes.decode("ascii", errors="ignore").strip()
                if coding_history:
                    bext_fields["CodingHistory"] = coding_history

            return bext_fields if bext_fields else None

        # Move to next chunk, maintaining alignment
        pos += 8 + ((chunk_size + 1) & ~1)

    return None


def _update_bext_field_in_riff_data(
    riff_data: bytearray, value: str | None, field_size: int, field_offset: int
) -> None:
    """Update a field in the bext chunk within RIFF data.

    This function modifies the riff_data bytearray in-place to update or create
    the bext chunk with the specified field. This is integrated into the main
    update flow to avoid multiple file writes.

    Args:
        riff_data: RIFF data bytearray (modified in-place)
        value: Field value to write, or None/empty string to clear
        field_size: Size of the field in bytes
        field_offset: Offset of the field within the bext chunk
    """
    encoded = (
        b"\x00" * field_size
        if value is None or value == ""
        else value.encode("utf-8")[: field_size - 1].ljust(field_size, b"\x00")
    )

    # Find bext chunk in RIFF data (no ID3v2 tags in riff_data at this point)
    pos = find_bext_chunk_in_riff_data(riff_data)
    if pos != -1:
        # Update existing bext chunk field
        bext_start = pos + 8
        riff_data[bext_start + field_offset : bext_start + field_offset + field_size] = encoded
    else:
        # No bext chunk, create one
        fmt_pos = find_fmt_chunk_in_riff_data(riff_data)
        if fmt_pos == -1:
            return  # Can't create bext without fmt chunk
        fmt_size = int.from_bytes(bytes(riff_data[fmt_pos + 4 : fmt_pos + 8]), "little")
        insert_pos = fmt_pos + 8 + fmt_size
        # Create bext chunk data: 602 bytes v1
        # Fill with zeros, then set the specific field
        bext_data = bytearray(b"bext" + (602).to_bytes(4, "little") + b"\x00" * 602)
        bext_data[8 + field_offset : 8 + field_offset + field_size] = encoded
        # Insert bext chunk after fmt chunk
        riff_data[insert_pos:insert_pos] = bext_data
        # Note: RIFF chunk size will be updated by caller after this method


def update_bext_description_in_riff_data(riff_data: bytearray, value: str | None) -> None:
    """Update the Description field in the bext chunk within RIFF data."""
    _update_bext_field_in_riff_data(riff_data, value, 256, 0)


def update_bext_originator_in_riff_data(riff_data: bytearray, value: str | None) -> None:
    """Update the Originator field in the bext chunk within RIFF data."""
    _update_bext_field_in_riff_data(riff_data, value, 32, 256)


def find_bext_chunk_in_riff_data(riff_data: bytearray) -> int:
    """Find the position of the bext chunk in RIFF data.

    Args:
        riff_data: RIFF data bytearray (no ID3v2 tags)

    Returns:
        Position of bext chunk, or -1 if not found
    """
    pos = 12  # Start after RIFF header (RIFF + size + WAVE = 12 bytes)
    while pos < len(riff_data) - 8:
        chunk_id = bytes(riff_data[pos : pos + 4])
        if chunk_id == b"bext":
            return pos
        chunk_size = int.from_bytes(bytes(riff_data[pos + 4 : pos + 8]), "little")
        pos += 8 + chunk_size
    return -1


def find_fmt_chunk_in_riff_data(riff_data: bytearray) -> int:
    """Find the position of the fmt chunk in RIFF data.

    Args:
        riff_data: RIFF data bytearray (no ID3v2 tags)

    Returns:
        Position of fmt chunk, or -1 if not found
    """
    pos = 12  # Start after RIFF header (RIFF + size + WAVE = 12 bytes)
    while pos < len(riff_data) - 8:
        chunk_id = bytes(riff_data[pos : pos + 4])
        if chunk_id == b"fmt ":
            return pos
        chunk_size = int.from_bytes(bytes(riff_data[pos + 4 : pos + 8]), "little")
        pos += 8 + chunk_size
    return -1


def find_bext_chunk(file_data: bytes, skip_id3v2_tags_func: Callable[[bytes], bytes]) -> int:
    """Find the position of the bext chunk in file data.

    Args:
        file_data: Full file data (may include ID3v2 tags)
        skip_id3v2_tags_func: Function to skip ID3v2 tags from file data

    Returns:
        Position of bext chunk, or -1 if not found
    """
    file_data = skip_id3v2_tags_func(file_data)
    pos = 12
    while pos < len(file_data) - 8:
        chunk_id = file_data[pos : pos + 4]
        if chunk_id == b"bext":
            return pos
        chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")
        pos += 8 + chunk_size
    return -1


def find_fmt_chunk(file_data: bytes, skip_id3v2_tags_func: Callable[[bytes], bytes]) -> int:
    """Find the position of the fmt chunk in file data.

    Args:
        file_data: Full file data (may include ID3v2 tags)
        skip_id3v2_tags_func: Function to skip ID3v2 tags from file data

    Returns:
        Position of fmt chunk, or -1 if not found
    """
    file_data = skip_id3v2_tags_func(file_data)
    pos = 12
    while pos < len(file_data) - 8:
        chunk_id = file_data[pos : pos + 4]
        if chunk_id == b"fmt ":
            return pos
        chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")
        pos += 8 + chunk_size
    return -1
