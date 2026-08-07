#!/usr/bin/env python3
"""Print ID3v1 fields from output/work/demo_read_id3v1.mp3 (other-tool style output for demos)."""
import sys
from pathlib import Path


def main() -> None:
    path = Path(__file__).resolve().parent.parent / "output" / "work" / "demo_read_id3v1.mp3"
    if not path.is_file():
        raise FileNotFoundError(
            "Run scripts/ensure_demo_read_id3v1.py first (missing output/work/demo_read_id3v1.mp3)",
        )
    data = path.read_bytes()
    if len(data) < 128 or data[-128:][:3] != b"TAG":
        sys.stdout.write("No ID3v1 tag.\n")
        return
    tag = data[-128:]
    title = tag[3:33].split(b"\x00", 1)[0].decode("latin-1", errors="replace").strip()
    artist = tag[33:63].split(b"\x00", 1)[0].decode("latin-1", errors="replace").strip()
    album = tag[63:93].split(b"\x00", 1)[0].decode("latin-1", errors="replace").strip()
    year = tag[93:97].split(b"\x00", 1)[0].decode("latin-1", errors="replace").strip()
    comment = tag[97:125].split(b"\x00", 1)[0].decode("latin-1", errors="replace").strip()
    sys.stdout.write(f"Title:  {title}\n")
    sys.stdout.write(f"Artist: {artist}\n")
    sys.stdout.write(f"Album:  {album}\n")
    sys.stdout.write(f"Year:   {year}\n")
    sys.stdout.write(f"Comment: {comment}\n")


if __name__ == "__main__":
    main()
