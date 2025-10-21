import pytest

from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa import get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLyricsDeleting:
    def test_delete_lyrics_id3v2(self):
        from audiometa import update_metadata
        from audiometa.utils.MetadataFormat import MetadataFormat
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using update_metadata
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            # Delete metadata by setting to None
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_id3v1(self):
        from audiometa.exceptions import MetadataNotSupportedError
        from audiometa import update_metadata
        from audiometa.utils.MetadataFormat import MetadataFormat
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # ID3v1 doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_lyrics_riff(self):
        from audiometa.exceptions import MetadataNotSupportedError
        from audiometa import update_metadata
        from audiometa.utils.MetadataFormat import MetadataFormat
        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by RIFF format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.RIFF)

    def test_delete_lyrics_vorbis(self):
        from audiometa.exceptions import MetadataNotSupportedError
        from audiometa import update_metadata
        from audiometa.utils.MetadataFormat import MetadataFormat
        
        with TempFileWithMetadata({}, "flac") as test_file:
            # Vorbis doesn't support lyrics in this implementation, so writing should fail
            with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.VORBIS)

    def test_delete_lyrics_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            test_file.set_id3v2_lyrics("Test lyrics")
            test_file.set_id3v2_title("Test Title")
            test_file.set_id3v2_artist("Test Artist")
        
            # Delete only lyrics using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS) == ["Test Artist"]

    def test_delete_lyrics_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete lyrics that don't exist
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set empty lyrics using helper method
            test_file.set_id3v2_lyrics("")
            # Delete the empty lyrics using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
