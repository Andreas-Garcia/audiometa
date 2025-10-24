import pytest

from audiometa import get_unified_metadata_field
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestAlbumArtistsReading:
    def test_id3v1(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v1") as test_file:
            album_artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists is None

    def test_id3v2(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_max_metadata()
            album_artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists == ["a" * 1000]

    def test_vorbis(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_max_metadata()
            album_artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists == ["a" * 1000]

    def test_riff(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_max_metadata()
            album_artists = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists == ["a" * 1000]
