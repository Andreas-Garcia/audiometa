import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLyricsDeleting:
    def test_delete_lyrics_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using helper method
            test_file.set_id3v2_lyrics("Test lyrics")
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            # Delete metadata using helper method
            test_file.delete_id3v2_lyrics()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # ID3v1 doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_id3v1_lyrics("Test lyrics")
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_id3v1_lyrics()

    def test_delete_lyrics_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_riff_lyrics("Test lyrics")
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_riff_lyrics()

    def test_delete_lyrics_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        
        with TempFileWithMetadata({}, "flac") as test_file:
            # Vorbis doesn't support lyrics in this implementation, so writing should fail
            with pytest.raises(MetadataNotSupportedError):
                test_file.set_vorbis_lyrics("Test lyrics")
            
            # Deleting should also fail since the field isn't supported
            with pytest.raises(MetadataNotSupportedError):
                test_file.delete_vorbis_lyrics()

    def test_delete_lyrics_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_lyrics("Test lyrics")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            # Delete only lyrics using helper method
            test_file.delete_id3v2_lyrics()
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_lyrics_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete lyrics that don't exist
            test_file.delete_id3v2_lyrics()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty lyrics using helper method
            test_file.set_id3v2_lyrics("")
            # Delete the empty lyrics
            test_file.delete_id3v2_lyrics()
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
