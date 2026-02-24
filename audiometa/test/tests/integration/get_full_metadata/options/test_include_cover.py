"""Tests for get_full_metadata include_cover option."""

from pathlib import Path

import pytest

from audiometa import get_full_metadata


@pytest.mark.integration
class TestGetFullMetadataIncludeCover:
    def test_get_full_metadata_exclude_cover(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file, include_cover=False)
        raw_id3v2 = result.get("raw_metadata", {}).get("id3v2", {})
        frames = raw_id3v2.get("frames", {})
        assert "APIC:" not in frames

    def test_get_full_metadata_include_cover_default(self, sample_mp3_file: Path):
        result = get_full_metadata(sample_mp3_file)
        raw_id3v2 = result.get("raw_metadata", {}).get("id3v2", {})
        assert "frames" in raw_id3v2

    def test_get_full_metadata_exclude_cover_riff(self, sample_wav_file: Path):
        result = get_full_metadata(sample_wav_file, include_cover=False)
        riff_raw = result.get("raw_metadata", {}).get("riff", {})
        parsed = riff_raw.get("parsed_fields", {})
        chunk = riff_raw.get("chunk_structure", {})
        assert "ICON" not in parsed
        assert "cover" not in chunk
        assert "image" not in chunk
