"""Sanitize raw metadata for get_full_metadata output (binary/opaque data as placeholders)."""

_ID3V2_BINARY_FRAME_PREFIXES = frozenset(
    {
        "APIC:",
        "GEOB:",
        "AENC:",
        "RVA2:",
        "RVRB:",
        "EQU2:",
        "PCNT:",
        "POPM:",
        "RBUF:",
        "LINK:",
        "POSS:",
        "SYLT:",
        "USLT:",
        "SYTC:",
        "ETCO:",
        "MLLT:",
        "OWNE:",
        "COMR:",
        "ENCR:",
        "GRID:",
        "PRIV:",
        "SIGN:",
        "SEEK:",
        "ASPI:",
    }
)

_VORBIS_OPAQUE_COMMENT_KEYS = frozenset({"TRAKTOR4"})

_ASCII_SPACE = 32


def _vorbis_value_has_binary(s: str) -> bool:
    return any(ord(c) < _ASCII_SPACE and c not in "\t\n\r" for c in s)


def sanitize_raw_info_for_full_metadata(raw_info: dict, format_key: str) -> dict:
    """Return a copy of raw_info with binary/opaque content replaced by size placeholders."""
    if format_key == "id3v2":
        return sanitize_id3v2_raw_info(raw_info)
    if format_key == "vorbis":
        return sanitize_vorbis_raw_info(raw_info)
    return raw_info


def sanitize_id3v2_raw_info(raw_info: dict) -> dict:
    result = dict(raw_info)
    frames = result.get("frames", {})
    if not frames:
        return result
    sanitized_frames = {}
    for frame_id, frame_data in frames.items():
        if any(frame_id.startswith(prefix) for prefix in _ID3V2_BINARY_FRAME_PREFIXES):
            size = frame_data.get("size", 0)
            flags = frame_data.get("flags", 0)
            sanitized_frames[frame_id] = {
                "text": f"<Binary data: {size} bytes>",
                "size": size,
                "flags": flags,
            }
        else:
            sanitized_frames[frame_id] = frame_data
    result["frames"] = sanitized_frames
    return result


def sanitize_vorbis_raw_info(raw_info: dict) -> dict:
    result = dict(raw_info)
    comments = result.get("comments", {})
    if not comments:
        return result
    sanitized: dict[str, list[str]] = {}
    for key, values in comments.items():
        key_str = str(key) if not isinstance(key, str) else key
        if not values:
            sanitized[key_str] = []
            continue
        if key_str in _VORBIS_OPAQUE_COMMENT_KEYS:
            total_bytes = sum(len(str(v).encode("utf-8")) for v in values)
            sanitized[key_str] = [f"<Binary or opaque data: {total_bytes} bytes>"]
            continue
        out: list[str] = []
        for v in values:
            s = str(v) if not isinstance(v, str) else v
            if _vorbis_value_has_binary(s):
                out.append(f"<Binary data: {len(s.encode('utf-8'))} bytes>")
            else:
                out.append(s)
        sanitized[key_str] = out
    result["comments"] = sanitized
    return result
