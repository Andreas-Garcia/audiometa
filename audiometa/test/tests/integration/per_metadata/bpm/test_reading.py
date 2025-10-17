

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestBpmReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        bpm = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.BPM)
        assert bpm is None

    def test_id3v2(self, metadata_id3v2_small_mp3):
        bpm = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.BPM)
        assert bpm == 999

    def test_vorbis(self, metadata_vorbis_small_flac):
        bpm = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.BPM)
        assert bpm == 999

    def test_riff(self, metadata_riff_small_wav):
        bpm = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.BPM)
        assert bpm is None
