import pytest

from audiometa import update_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import MetadataFieldNotSupportedByMetadataFormatError
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLyricsDeleting:
    def test_delete_lyrics_id3v2(self):        
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_lyrics(test_file.path, "Test lyrics")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=Test lyrics" in raw_metadata
        
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=Test lyrics" not in raw_metadata

    def test_delete_lyrics_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # ID3v1 doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V1)

    def test_delete_lyrics_riff(self):        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.LYRICS metadata not supported by RIFF format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.RIFF)

    def test_delete_lyrics_vorbis(self):        
        with TempFileWithMetadata({}, "flac") as test_file:
            # Vorbis doesn't support lyrics in this implementation, so writing should fail
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.VORBIS)

    def test_delete_lyrics_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            ID3v2MetadataSetter.set_lyrics("Test lyrics")
            ID3v2MetadataSetter.set_title("Test Title")
            ID3v2MetadataSetter.set_artists("Test Artist")

            # Delete only lyrics using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=Test lyrics" not in raw_metadata
            assert "TIT2=Test Title" in raw_metadata
            assert "TPE1=Test Artist" in raw_metadata

    def test_delete_lyrics_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete lyrics that don't exist
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" not in raw_metadata
            
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)

            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" not in raw_metadata
            
    def test_delete_lyrics_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_lyrics("")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" in raw_metadata  # Empty lyrics field exists
            
            update_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" not in raw_metadata
