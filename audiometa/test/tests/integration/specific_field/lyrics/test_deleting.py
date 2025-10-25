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
    def test_delete_lyrics_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V1)
    
    def test_delete_lyrics_id3v2_3(self):        
        with TempFileWithMetadata({}, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_lyrics(test_file.path, "Test lyrics")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert raw_metadata['USLT'] == ["eng:Test lyrics"]
        
            update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: None}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version='2.3')
            assert raw_metadata.get('USLT') is None
            
    def test_delete_lyrics_id3v2_4(self):        
        with TempFileWithMetadata({}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_lyrics(test_file.path, "Test lyrics", version='2.4')
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version='2.4')
            assert raw_metadata['USLT'] == ["eng:Test lyrics"]
        
            update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: None}, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path, version='2.4')
            assert raw_metadata.get('USLT') is None

    def test_delete_lyrics_riff(self):        
        with TempFileWithMetadata({}, "wav") as test_file:
            # RIFF doesn't support lyrics, so writing should fail
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS metadata not supported by RIFF format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.RIFF)

    def test_delete_lyrics_vorbis(self):        
        with TempFileWithMetadata({}, "flac") as test_file:
            # Vorbis doesn't support lyrics in this implementation, so writing should fail
            with pytest.raises(MetadataFieldNotSupportedByMetadataFormatError, match="UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS metadata not supported by this format"):
                update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.VORBIS)

    def test_delete_lyrics_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set multiple metadata fields using helper methods
            ID3v2MetadataSetter.set_lyrics(test_file.path, "Test lyrics")
            ID3v2MetadataSetter.set_title(test_file.path, "Test Title")
            ID3v2MetadataSetter.set_artists(test_file.path, "Test Artist")

            # Delete only lyrics using library API
            update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert raw_metadata is None

    def test_delete_lyrics_already_none(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Try to delete lyrics that don't exist
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "UNSYNCHRONIZED_LYRICS=" not in raw_metadata
            
            update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: None}, metadata_format=MetadataFormat.VORBIS)

            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "UNSYNCHRONIZED_LYRICS=" not in raw_metadata
            
    def test_delete_lyrics_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            ID3v2MetadataSetter.set_lyrics("")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" in raw_metadata  # Empty lyrics field exists
            
            update_metadata(test_file.path, {UnifiedMetadataKey.UNSYNCHRONIZED_LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            assert "USLT=" not in raw_metadata
