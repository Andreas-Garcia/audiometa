import pytest

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestAlbumDeleting:
    def test_delete_album_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: "Test Album"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_id3v1(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: "Test Album"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: "Test Album"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: "Test Album"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.ALBUM_NAME: "Test Album",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
            
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None})
            
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_album_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
