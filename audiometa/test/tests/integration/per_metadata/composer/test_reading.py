"""Tests for reading composer metadata."""

import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestComposerReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        composer = metadata.get(UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        composer = metadata.get(UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        composer = metadata.get(UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_riff(self, metadata_riff_small_wav):
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        composer = metadata.get(UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)
