#!/usr/bin/env python3
"""Align samples/sample.mp3 and samples/sample.flac to the same canonical track metadata."""

from pathlib import Path

from audiometa import update_metadata
from audiometa.utils.metadata_writing_strategy import MetadataWritingStrategy
from audiometa.utils.unified_metadata_key import UnifiedMetadataKey

_CANONICAL: dict[UnifiedMetadataKey, object] = {
    UnifiedMetadataKey.TITLE: "We Are the Champions",
    UnifiedMetadataKey.ARTISTS: ["Queen"],
    UnifiedMetadataKey.ALBUM: "News of the World",
    UnifiedMetadataKey.ALBUM_ARTISTS: ["Queen"],
    UnifiedMetadataKey.RELEASE_DATE: "1977-10-28",
    UnifiedMetadataKey.TRACK_NUMBER: "4/11",
    UnifiedMetadataKey.DISC_NUMBER: 1,
    UnifiedMetadataKey.DISC_TOTAL: 1,
    UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Arena Rock"],
    UnifiedMetadataKey.LANGUAGE: "eng",
}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    samples = root / "samples"
    for name in ("sample.mp3", "sample.flac"):
        path = samples / name
        if not path.is_file():
            raise FileNotFoundError(str(path))
        update_metadata(path, _CANONICAL, metadata_strategy=MetadataWritingStrategy.SYNC)


if __name__ == "__main__":
    main()
