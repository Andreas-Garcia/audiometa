

import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestArtistsReading:
    def test_id3v1(self, metadata_id3v1_small_mp3):
        artists = get_specific_metadata(metadata_id3v1_small_mp3, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)

    def test_id3v2(self, metadata_id3v2_small_mp3):
        artists = get_specific_metadata(metadata_id3v2_small_mp3, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)

    def test_vorbis(self, metadata_vorbis_small_flac):
        artists = get_specific_metadata(metadata_vorbis_small_flac, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)

    def test_riff(self, metadata_riff_small_wav):
        artists = get_specific_metadata(metadata_riff_small_wav, UnifiedMetadataKey.ARTISTS_NAMES)
        assert artists is None or isinstance(artists, list)
