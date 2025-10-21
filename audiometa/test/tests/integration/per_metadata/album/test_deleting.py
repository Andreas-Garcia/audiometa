import pytest

from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestAlbumDeleting:
    def test_delete_album_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_id3v1(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            test_file.set_id3v1_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_file.set_riff_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_file.set_vorbis_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_album("Test Album")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
            
            # Delete only album using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_album_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete album that doesn't exist
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_album("")
            # Delete the empty album using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_NAME: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
