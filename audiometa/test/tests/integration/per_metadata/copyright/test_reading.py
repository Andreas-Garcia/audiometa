

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestCopyrightReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        copyright_info = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info is None or isinstance(copyright_info, str)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        copyright_info = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info is None or isinstance(copyright_info, str)

    def test_vorbis(self, metadata_vorbis_small_flac):
        copyright_info = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info is None or isinstance(copyright_info, str)

    def test_riff(self, metadata_riff_small_wav):
        copyright_info = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info is None or isinstance(copyright_info, str)
