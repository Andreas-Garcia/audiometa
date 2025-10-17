import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestPublisherDeleting:
    def test_delete_publisher_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.PUBLISHER: "Test Publisher",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_publisher_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None
