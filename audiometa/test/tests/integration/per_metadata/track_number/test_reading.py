

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestTrackNumberReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        track_number = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, (int, str))

    def test_id3v2(self, metadata_id3v2_small_mp3):
        track_number = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, (int, str))

    def test_vorbis(self, metadata_vorbis_small_flac):
        track_number = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, (int, str))

    def test_riff(self, metadata_riff_small_wav):
        track_number = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.TRACK_NUMBER)
        assert track_number is None or isinstance(track_number, (int, str))
