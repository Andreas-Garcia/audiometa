"""INFO chunk operations for RIFF files.

This module handles reading and writing of RIFF INFO chunks, which contain
standard metadata fields like title, artist, album, etc.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from ....utils.types import RawMetadataKey

if TYPE_CHECKING:
    pass

from ._riff_constants import RIFF_CHUNK_ID_SIZE, RIFF_HEADER_SIZE, RIFF_WAVE_FORMAT_POSITION


def extract_riff_metadata_directly(
    file_data: bytes, skip_id3v2_tags_func: Callable[[bytes], bytes], riff_tag_key_class: type[object]
) -> dict[str, list[str]]:
    """Manually extract metadata from RIFF chunks without relying on external libraries.

    This function directly parses the RIFF structure to extract metadata from the INFO chunk.

    Args:
        file_data: Full file data (may include ID3v2 tags)
        skip_id3v2_tags_func: Function to skip ID3v2 tags from file data
        riff_tag_key_class: RiffTagKey class for validation

    Returns:
        Dictionary mapping RIFF tag IDs to lists of values
    """
    info_tags: dict[str, list[str]] = {}

    # Skip ID3v2 if present
    file_data = skip_id3v2_tags_func(file_data)

    # Validate RIFF header
    if (
        len(file_data) < RIFF_HEADER_SIZE
        or file_data[:RIFF_CHUNK_ID_SIZE] != b"RIFF"
        or file_data[RIFF_WAVE_FORMAT_POSITION:RIFF_HEADER_SIZE] != b"WAVE"
    ):
        return info_tags

    pos = 12  # Start after RIFF header
    while pos < len(file_data) - 8:
        chunk_id = file_data[pos : pos + 4]
        chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")

        if chunk_id == b"LIST" and pos + 12 <= len(file_data) and file_data[pos + 8 : pos + 12] == b"INFO":
            # Process INFO chunk
            info_pos = pos + 12
            info_end = pos + 8 + chunk_size

            while info_pos < info_end - 8:
                # Extract each metadata field
                field_id = file_data[info_pos : info_pos + 4].decode("ascii", errors="ignore")
                field_size = int.from_bytes(file_data[info_pos + 4 : info_pos + 8], "little")

                if field_size > 0 and info_pos + 8 + field_size <= info_end:
                    # -1 to exclude null terminator
                    field_data = file_data[info_pos + 8 : info_pos + 8 + field_size - 1]
                    try:
                        # Decode and handle null-terminated strings
                        field_value = field_data.decode("utf-8", errors="ignore")
                        # Split on null byte and take first part if exists
                        field_value = field_value.split("\x00")[0].strip()
                        # Compare field_id with enum member values (FourCC strings)
                        # Use getattr to safely access __members__ for type checking
                        members = getattr(riff_tag_key_class, "__members__", {})
                        if any(field_id == member.value for member in cast(dict, members).values()) and field_value:
                            if field_id not in info_tags:
                                info_tags[field_id] = []
                            info_tags[field_id].append(field_value)
                    except UnicodeDecodeError:
                        pass

                # Move to next field, maintaining alignment
                info_pos += 8 + ((field_size + 1) & ~1)
            break

        # Move to next chunk, maintaining alignment
        pos += 8 + ((chunk_size + 1) & ~1)

    return info_tags


def find_info_chunk_in_file_data(file_data: bytearray) -> int:
    """Find the position of the INFO chunk in RIFF data.

    Args:
        file_data: RIFF data bytearray

    Returns:
        Position of INFO chunk, or -1 if not found
    """
    pos = 12  # Start after RIFF header
    while pos < len(file_data) - 8:
        if (
            bytes(file_data[pos : pos + 4]) == b"LIST"
            and pos + 8 < len(file_data)
            and bytes(file_data[pos + 8 : pos + 12]) == b"INFO"
        ):
            return pos
        chunk_size = int.from_bytes(bytes(file_data[pos + 4 : pos + 8]), "little")
        pos += 8 + ((chunk_size + 1) & ~1)  # Move to next chunk, maintaining alignment
    return -1


def create_info_chunk_after_wave_header(file_data: bytearray) -> int:
    """Create a minimal INFO chunk after the WAVE header.

    Args:
        file_data: RIFF data bytearray (modified in-place)

    Returns:
        Position where INFO chunk was inserted
    """
    info_chunk = bytearray(b"LIST\x04\x00\x00\x00INFO")  # Minimal INFO chunk
    insert_pos = 12  # After RIFF+size+WAVE
    file_data[insert_pos:insert_pos] = info_chunk
    return insert_pos


def create_aligned_metadata_with_proper_padding(metadata_id: RawMetadataKey, value_bytes: bytes) -> bytes:
    """Create properly aligned metadata entry with padding.

    Args:
        metadata_id: RIFF tag key (FourCC)
        value_bytes: Tag value as bytes

    Returns:
        Properly formatted and aligned metadata entry
    """
    # Add null terminator
    value_bytes = value_bytes + b"\x00"
    # Pad to even length if needed
    if len(value_bytes) % 2:
        value_bytes = value_bytes + b"\x00"

    return metadata_id.encode("ascii") + len(value_bytes).to_bytes(4, "little") + value_bytes


def update_info_chunk_in_riff_data(riff_data: bytearray, info_chunk_start: int, new_tags_data: bytearray) -> None:
    """Update INFO chunk in RIFF data with new tags.

    Args:
        riff_data: RIFF data bytearray (modified in-place)
        info_chunk_start: Start position of existing INFO chunk
        new_tags_data: New tags data to write
    """
    info_chunk_size = int.from_bytes(bytes(riff_data[info_chunk_start + 4 : info_chunk_start + 8]), "little")

    # Create new INFO chunk
    new_info_chunk = bytearray()
    new_info_chunk.extend(b"LIST")
    new_info_chunk.extend((len(new_tags_data) + 4).to_bytes(4, "little"))  # +4 for 'INFO'
    new_info_chunk.extend(b"INFO")
    new_info_chunk.extend(new_tags_data)

    # Replace old INFO chunk in RIFF data
    riff_data[info_chunk_start : info_chunk_start + info_chunk_size + 8] = new_info_chunk
