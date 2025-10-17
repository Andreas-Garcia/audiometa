import pytest

from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestAlbumDeleting:
    def test_delete_album_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using helper method
            test_file.delete_id3v2_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_id3v1(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            # Set metadata using helper method
            test_file.set_id3v1_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using helper method
            test_file.delete_id3v1_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set metadata using helper method
            test_file.set_riff_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using helper method
            test_file.delete_riff_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using helper method
            test_file.set_vorbis_album("Test Album")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"
            
            # Delete metadata using helper method
            test_file.delete_vorbis_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_album("Test Album")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
            
            # Delete only album using helper method
            test_file.delete_id3v2_album()
            
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_album_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete album that doesn't exist
            test_file.delete_id3v2_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None

    def test_delete_album_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty album using helper method
            test_file.set_id3v2_album("")
            # Delete the empty album
            test_file.delete_id3v2_album()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) is None
