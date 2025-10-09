"""Tests for reading BPM metadata."""

import pytest

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBpmReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        bpm = metadata.get(UnifiedMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, (int, float))

    def test_id3v2(self, metadata_id3v2_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        bpm = metadata.get(UnifiedMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, (int, float))

    def test_vorbis(self, metadata_vorbis_small_flac):
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        bpm = metadata.get(UnifiedMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, (int, float))

    def test_riff(self, metadata_riff_small_wav):
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        bpm = metadata.get(UnifiedMetadataKey.BPM)
        assert bpm is None or isinstance(bpm, (int, float))
