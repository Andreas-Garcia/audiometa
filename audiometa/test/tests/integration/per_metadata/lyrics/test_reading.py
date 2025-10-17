it

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLyricsReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        lyrics = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        lyrics = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        lyrics = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)

    def test_riff(self, metadata_riff_small_wav):
        lyrics = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)
