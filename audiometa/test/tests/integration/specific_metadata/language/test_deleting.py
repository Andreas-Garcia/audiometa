import pytest

from audiometa import get_unified_metadata_field, update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLanguageDeleting:
    def test_delete_language_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_language("en")
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "id3v1") as test_file:
            # Deleting should fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_language_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            test_file.set_riff_language("en")
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.RIFF)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            test_file.set_vorbis_language("en")
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_language("en")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
            
            # Delete only language using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
            
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.ARTISTS) == ["Test Artist"]

    def test_delete_language_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete language that doesn't exist
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            test_file.set_id3v2_language("")
            # Delete the empty language using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LANGUAGE: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_unified_metadata_field(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
