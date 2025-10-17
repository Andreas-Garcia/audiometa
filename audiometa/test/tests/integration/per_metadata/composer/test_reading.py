

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestComposerReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        composer = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        composer = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        composer = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)

    def test_riff(self, metadata_riff_small_wav):
        composer = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)
