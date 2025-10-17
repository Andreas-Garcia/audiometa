import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestTitleDeleting:
    def test_delete_title_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: "Test Title"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: "Test Title"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: "Test Title"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: "Test Title"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Test Album"
            })
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_delete_title_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.TITLE: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None
