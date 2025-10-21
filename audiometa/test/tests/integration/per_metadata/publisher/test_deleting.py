import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestPublisherDeleting:
    def test_delete_publisher_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) == "Test Publisher"
        
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # ID3v1 format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.PUBLISHER metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_publisher_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.PUBLISHER metadata not supported by RIFF format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.RIFF)

    def test_delete_publisher_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            # Vorbis format raises exception for unsupported metadata
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.PUBLISHER metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}, metadata_format=MetadataFormat.VORBIS)

    def test_delete_publisher_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {
                UnifiedMetadataKey.PUBLISHER: "Test Publisher",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
        
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_publisher_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None

    def test_delete_publisher_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: ""})
            update_metadata(test_file.path, {UnifiedMetadataKey.PUBLISHER: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.PUBLISHER) is None
