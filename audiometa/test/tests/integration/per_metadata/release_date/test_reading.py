

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestReleaseDateReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        release_date = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        release_date = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        release_date = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)

    def test_riff(self, metadata_riff_small_wav):
        release_date = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.RELEASE_DATE)
        assert release_date is None or isinstance(release_date, str)
