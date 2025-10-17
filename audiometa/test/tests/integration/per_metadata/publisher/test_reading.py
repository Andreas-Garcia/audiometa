

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestPublisherReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        publisher = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        publisher = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        publisher = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)

    def test_riff(self, metadata_riff_small_wav):
        publisher = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)
