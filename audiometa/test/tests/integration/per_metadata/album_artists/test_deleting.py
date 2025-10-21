import pytest

from audiometa import get_specific_metadata, update_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestAlbumArtistsDeleting:
    def test_delete_album_artists_id3v2(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using max metadata method (includes album artists)
            test_file.set_id3v2_max_metadata()
            # Verify album artists are set
            album_artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists is not None
        
            # Delete metadata by setting to None
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None

    def test_delete_album_artists_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Set metadata using max metadata method (includes album artists)
            test_file.set_riff_max_metadata()
            # Verify album artists are set
            album_artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists is not None
        
            # Delete metadata by setting to None
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.RIFF)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None

    def test_delete_album_artists_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Set metadata using max metadata method (includes album artists)
            test_file.set_vorbis_max_metadata()
            # Verify album artists are set
            album_artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists is not None
        
            # Delete metadata by setting to None
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.VORBIS)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None

    def test_delete_album_artists_preserves_other_fields(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using max metadata method (includes album artists and other fields)
            test_file.set_id3v2_max_metadata()
            # Verify album artists are set
            album_artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS)
            assert album_artists is not None
        
            # Delete only album artists
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.ID3V2)
        
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None
            # Verify other fields are preserved
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE)
            assert title is not None

    def test_delete_album_artists_already_none(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Try to delete album artists that don't exist
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None

    def test_delete_album_artists_empty_list(self):
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Set metadata using max metadata method (includes album artists)
            test_file.set_id3v2_max_metadata()
            # Delete the album artists
            update_metadata(test_file.path, {UnifiedMetadataKey.ALBUM_ARTISTS: None}, metadata_format=MetadataFormat.ID3V2)
            assert get_specific_metadata(test_file.path, UnifiedMetadataKey.ALBUM_ARTISTS) is None
