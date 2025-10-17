import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestCommentDeleting:
    def test_delete_comment_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_comment("Test comment")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            # Delete metadata using helper method
            test_file.delete_id3v2_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v1_comment("Test comment")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            # Delete metadata using helper method
            test_file.delete_id3v1_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set metadata using helper method
            test_file.set_riff_comment("Test comment")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            # Delete metadata using helper method
            test_file.delete_riff_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using helper method
            test_file.set_vorbis_comment("Test comment")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) == "Test comment"
        
            # Delete metadata using helper method
            test_file.delete_vorbis_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_comment("Test comment")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            # Delete only comment using helper method
            test_file.delete_id3v2_comment()
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_comment_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete comment that doesn't exist
            test_file.delete_id3v2_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None

    def test_delete_comment_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty comment using helper method
            test_file.set_id3v2_comment("")
            # Delete the empty comment
            test_file.delete_id3v2_comment()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.COMMENT) is None
