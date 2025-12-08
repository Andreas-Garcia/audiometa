"""RIFF file structure utilities.

This module handles RIFF file structure operations like ID3v2 tag handling,
chunk finding, and file reconstruction.
"""

from collections.abc import Callable

from ..id3v2._id3v2_constants import ID3V2_HEADER_SIZE
from ._riff_constants import RIFF_CHUNK_ID_SIZE, RIFF_HEADER_SIZE, RIFF_WAVE_FORMAT_POSITION


def skip_id3v2_tags(data: bytes) -> bytes:
    """Skip ID3v2 tags at the beginning of file data.

    Args:
        data: File data that may start with ID3v2 tags

    Returns:
        File data with ID3v2 tags skipped
    """
    if data.startswith(b"ID3"):
        if len(data) < ID3V2_HEADER_SIZE:
            return data
        # Get size from synchsafe integer (7 bits per byte)
        size_bytes = data[6:ID3V2_HEADER_SIZE]
        size = (
            ((size_bytes[0] & 0x7F) << 21)
            | ((size_bytes[1] & 0x7F) << 14)
            | ((size_bytes[2] & 0x7F) << 7)
            | (size_bytes[3] & 0x7F)
        )
        # Skip the header (10 bytes) plus the size of the tag
        return data[ID3V2_HEADER_SIZE + size :]
    return data


def extract_and_validate_riff_data(
    file_data: bytearray, should_preserve_id3v2: bool, find_riff_header_after_id3v2_func: Callable[[bytearray], int]
) -> bytearray:
    """Extract RIFF data from file data and validate format.

    Args:
        file_data: Full file data including potential ID3v2 tags
        should_preserve_id3v2: Whether to preserve ID3v2 tags
        find_riff_header_after_id3v2_func: Function to find RIFF header after ID3v2

    Returns:
        RIFF data bytearray

    Raises:
        MetadataFieldNotSupportedByMetadataFormatError: If RIFF format is invalid
    """
    from ....exceptions import MetadataFieldNotSupportedByMetadataFormatError

    if should_preserve_id3v2 and file_data.startswith(b"ID3"):
        # Find RIFF header after ID3v2 tags
        riff_start = find_riff_header_after_id3v2_func(file_data)
        if riff_start == -1:
            msg = "Invalid WAV file format - RIFF header not found after ID3v2 tags"
            raise MetadataFieldNotSupportedByMetadataFormatError(msg)
        riff_data = file_data[riff_start:]
    else:
        riff_data = file_data

    if (
        len(riff_data) < RIFF_HEADER_SIZE
        or bytes(riff_data[:RIFF_CHUNK_ID_SIZE]) != b"RIFF"
        or bytes(riff_data[RIFF_WAVE_FORMAT_POSITION:RIFF_HEADER_SIZE]) != b"WAVE"
    ):
        msg = "Invalid WAV file format"
        raise MetadataFieldNotSupportedByMetadataFormatError(msg)

    return riff_data


def update_riff_chunk_size(riff_data: bytearray) -> None:
    """Update RIFF chunk size in RIFF data.

    Args:
        riff_data: RIFF data bytearray (modified in-place)
    """
    total_size = len(riff_data) - 8  # Exclude RIFF and size fields
    riff_data[4:8] = total_size.to_bytes(4, "little")


def reconstruct_final_file_data(
    file_data: bytearray,
    riff_data: bytearray,
    should_preserve_id3v2: bool,
    get_id3v2_size_func: Callable[[bytearray], int],
) -> bytearray:
    """Reconstruct final file data with ID3v2 tags if needed.

    Args:
        file_data: Original file data
        riff_data: Updated RIFF data
        should_preserve_id3v2: Whether ID3v2 tags should be preserved
        get_id3v2_size_func: Function to get ID3v2 tag size

    Returns:
        Final file data ready to write
    """
    if should_preserve_id3v2 and file_data.startswith(b"ID3"):
        # Reconstruct the full file with ID3v2 tags + updated RIFF data
        id3v2_size = get_id3v2_size_func(file_data)
        final_file_data = bytearray(file_data[:id3v2_size])  # Keep ID3v2 tags
        final_file_data.extend(riff_data)  # Add updated RIFF data
        return final_file_data
    return riff_data


def find_riff_header_after_id3v2(file_data: bytearray) -> int:
    """Find the position of the RIFF header after ID3v2 tags.

    Args:
        file_data: Full file data starting with ID3v2 tags

    Returns:
        Position of RIFF header, or -1 if not found
    """
    if not file_data.startswith(b"ID3"):
        return -1

    # Skip ID3v2 tags using existing function
    skipped_data = skip_id3v2_tags(bytes(file_data))
    if not skipped_data.startswith(b"RIFF"):
        return -1

    # Calculate the position where RIFF starts
    return len(file_data) - len(skipped_data)


def get_id3v2_size(file_data: bytearray) -> int:
    """Get the size of ID3v2 tags in file data.

    Args:
        file_data: File data starting with ID3v2 tags

    Returns:
        Size of ID3v2 tags in bytes (including header)
    """
    if not file_data.startswith(b"ID3"):
        return 0

    if len(file_data) < ID3V2_HEADER_SIZE:
        return 0

    # Get size from synchsafe integer (7 bits per byte)
    size_bytes = file_data[6:ID3V2_HEADER_SIZE]
    size = (
        ((size_bytes[0] & 0x7F) << 21)
        | ((size_bytes[1] & 0x7F) << 14)
        | ((size_bytes[2] & 0x7F) << 7)
        | (size_bytes[3] & 0x7F)
    )

    return 10 + size  # Header (10 bytes) + data size
