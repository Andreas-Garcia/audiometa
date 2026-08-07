#!/usr/bin/env python3
"""Build output/work/demo_read_id3v1.mp3 from samples/sample.mp3 (ID3v2/v1 stripped; new ID3v1 only)."""
from pathlib import Path


def _strip_id3v2(data: bytes) -> bytes:
    while len(data) >= 10 and data[:3] == b"ID3":
        size = (data[6] & 0x7F) << 21 | (data[7] & 0x7F) << 14 | (data[8] & 0x7F) << 7 | (data[9] & 0x7F)
        footer_size = 10 if data[5] & 0x10 else 0
        data = data[10 + size + footer_size :]
    return data


def _strip_id3v1(data: bytes) -> bytes:
    if len(data) >= 128 and data[-128:][:3] == b"TAG":
        return data[:-128]
    return data


def _field(text: str, length: int) -> bytes:
    return text.encode("latin-1", errors="replace")[:length].ljust(length, b"\x00")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    src = root / "samples" / "sample.mp3"
    out_dir = root / "output" / "work"
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "demo_read_id3v1.mp3"
    if not src.is_file():
        raise FileNotFoundError(str(src))
    data = _strip_id3v2(_strip_id3v1(src.read_bytes()))
    title = _field("We Are the Champions", 30)
    artist = _field("Queen", 30)
    album = _field("News of the World", 30)
    year = _field("1977", 4)
    comment = _field("", 28)
    tag = b"TAG" + title + artist + album + year + comment + b"\x00\x00\x00"
    if len(tag) != 128:
        raise ValueError(f"expected 128-byte ID3v1 tag, got {len(tag)}")
    dst.write_bytes(data + tag)


if __name__ == "__main__":
    main()
