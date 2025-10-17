import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestGenreDeleting:
    def test_delete_genre_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_genre("Rock")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) == ["Rock"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None

    def test_delete_genre_id3v1(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            test_file.set_id3v1_genre("Rock")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) == ["Rock"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None

    def test_delete_genre_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_file.set_riff_genre("Rock")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) == ["Rock"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None

    def test_delete_genre_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) == ["Rock"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None

    def test_delete_genre_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_genre("Rock")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.ID3V2)
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_genre_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None

    def test_delete_genre_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_genre("")
            update_file_metadata(test_file.path, {UnifiedMetadataKey.GENRE_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME) is None
