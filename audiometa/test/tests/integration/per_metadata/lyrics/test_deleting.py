import pytest



from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestLyricsDeleting:
    def test_delete_lyrics_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: "Test lyrics"}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) == "Test lyrics"
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.LYRICS: "Test lyrics",
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
            })
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_lyrics_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None

    def test_delete_lyrics_empty_string(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: ""})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.LYRICS: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.LYRICS) is None
