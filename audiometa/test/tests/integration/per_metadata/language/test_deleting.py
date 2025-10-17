import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestLanguageDeleting:
    def test_delete_language_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_language("en")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using helper method
            test_file.delete_id3v2_language()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "id3v1") as test_file:
            # ID3v1 doesn't support language, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_id3v1_language("en")
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_id3v1_language()

    def test_delete_language_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set metadata using helper method
            test_file.set_riff_language("en")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using helper method
            test_file.delete_riff_language()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using helper method
            test_file.set_vorbis_language("en")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) == "en"
            
            # Delete metadata using helper method
            test_file.delete_vorbis_language()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_language("en")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
            
            # Delete only language using helper method
            test_file.delete_id3v2_language()
            
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_language_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete language that doesn't exist
            test_file.delete_id3v2_language()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None

    def test_delete_language_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty language using helper method
            test_file.set_id3v2_language("")
            # Delete the empty language
            test_file.delete_id3v2_language()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LANGUAGE) is None
