#!/usr/bin/env python3
"""Build demo_read_id3v1.mp3: MPEG audio from sample.mp3 with tags stripped and a fresh ID3v1 tag only."""
from pathlib import Path


def _strip_id3v2(data: bytes) -> bytes:
    while len(data) >= 10 and data[:3] == b"ID3":
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
        data = data[10 + size :]
    return data


def _strip_id3v1(data: bytes) -> bytes:
    if len(data) >= 128 and data[-128:][:3] == b"TAG":
        return data[:-128]
    return data


def _field(text: str, length: int) -> bytes:
    return text.encode("latin-1", errors="replace")[:length].ljust(length, b"\x00")


def main() -> None:
    root = Path(__file__).resolve().parent
    src = root / "sample.mp3"
    dst = root / "demo_read_id3v1.mp3"
    if not src.is_file():
        raise FileNotFoundError(str(src))
    data = _strip_id3v2(_strip_id3v1(src.read_bytes()))
    title = _field("Demo Title", 30)
    artist = _field("Demo Artist", 30)
    album = _field("", 30)
    year = _field("2025", 4)
    comment = _field("", 28)
    tag = b"TAG" + title + artist + album + year + comment + b"\x00\x00\x00"
    if len(tag) != 128:
        raise ValueError(f"expected 128-byte ID3v1 tag, got {len(tag)}")
    dst.write_bytes(data + tag)


if __name__ == "__main__":
    main()
