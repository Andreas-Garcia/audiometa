import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestTitleDeleting:
    def test_delete_title_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_title("Test Title")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            # Delete metadata using helper method
            test_file.delete_id3v2_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v1_title("Test Title")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            # Delete metadata using helper method
            test_file.delete_id3v1_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set metadata using helper method
            test_file.set_riff_title("Test Title")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            # Delete metadata using helper method
            test_file.delete_riff_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using helper method
            test_file.set_vorbis_title("Test Title")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
        
            # Delete metadata using helper method
            test_file.delete_vorbis_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
            test_file.set_id3v2_album("Test Album")
        
            # Delete only title using helper method
            test_file.delete_id3v2_title()
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_delete_title_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete title that doesn't exist
            test_file.delete_id3v2_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None

    def test_delete_title_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty title using helper method
            test_file.set_id3v2_title("")
            # Delete the empty title
            test_file.delete_id3v2_title()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) is None
