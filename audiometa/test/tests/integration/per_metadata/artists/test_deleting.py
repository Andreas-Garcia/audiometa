import pytest



from audiometa import get_specific_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestArtistsDeleting:
    def test_delete_artists_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"]}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1", "Artist 2"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_id3v1(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1"]}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.ID3V1)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1"]}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"]}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1", "Artist 2"]
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
                UnifiedMetadataKey.TITLE: "Test Title",
                UnifiedMetadataKey.ALBUM_NAME: "Test Album"
            })
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None})
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE) == "Test Title"
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_delete_artists_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_empty_list(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
        
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: []})
            update_file_metadata(test_file.path, {UnifiedMetadataKey.ARTISTS_NAMES: None})
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES) is None
