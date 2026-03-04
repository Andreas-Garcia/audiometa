"""INFO chunk operations for RIFF files.

This module handles reading and writing of RIFF INFO chunks, which contain
standard metadata fields like title, artist, album, etc.
"""

from collections.abc import Callable

from ....utils.types import RawMetadataKey
from ._riff_constants import RIFF_CHUNK_ID_SIZE, RIFF_HEADER_SIZE, RIFF_WAVE_FORMAT_POSITION

_FOURCC_MIN = 0x20
_FOURCC_MAX = 0x7E


def _is_valid_fourcc(fourcc_bytes: bytes) -> bool:
    """Return True if the 4 bytes form a valid INFO chunk FourCC (printable ASCII)."""
    if len(fourcc_bytes) != RIFF_CHUNK_ID_SIZE:
        return False
    return all(_FOURCC_MIN <= b <= _FOURCC_MAX for b in fourcc_bytes)


def extract_riff_metadata_directly(
    file_data: bytes, skip_id3v2_tags_func: Callable[[bytes], bytes]
) -> dict[str, list[str]]:
    """Manually extract metadata from RIFF chunks without relying on external libraries.

    Parses the RIFF structure and returns every INFO chunk field. No filtering by
    RiffTagKey—known and custom FourCCs are included. Only subchunks with a valid
    4-byte printable-ASCII FourCC are accepted.
    """
    info_tags: dict[str, list[str]] = {}

    file_data = skip_id3v2_tags_func(file_data)

    if (
        len(file_data) < RIFF_HEADER_SIZE
        or file_data[:RIFF_CHUNK_ID_SIZE] != b"RIFF"
        or file_data[RIFF_WAVE_FORMAT_POSITION:RIFF_HEADER_SIZE] != b"WAVE"
    ):
        return info_tags

    pos = 12
    while pos < len(file_data) - 8:
        chunk_id = file_data[pos : pos + 4]
        chunk_size = int.from_bytes(file_data[pos + 4 : pos + 8], "little")

        if chunk_id == b"LIST" and pos + 12 <= len(file_data) and file_data[pos + 8 : pos + 12] == b"INFO":
            info_pos = pos + 12
            info_end = pos + 8 + chunk_size

            while info_pos < info_end - 8:
                field_id_bytes = file_data[info_pos : info_pos + 4]
                field_size = int.from_bytes(file_data[info_pos + 4 : info_pos + 8], "little")

                if field_size > 0 and info_pos + 8 + field_size <= info_end and _is_valid_fourcc(field_id_bytes):
                    field_id = field_id_bytes.decode("ascii")
                    field_data = file_data[info_pos + 8 : info_pos + 8 + field_size - 1]
                    try:
                        field_value = field_data.decode("utf-8", errors="ignore").split("\x00")[0].strip()
                        if field_value:
                            if field_id not in info_tags:
                                info_tags[field_id] = []
                            info_tags[field_id].append(field_value)
                    except UnicodeDecodeError:
                        pass

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
