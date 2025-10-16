import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestArtistsDeleting:
    def test_delete_artists_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"]}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1", "Artist 2"]
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1"]}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1"]
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1"]}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1"]
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2"]}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Artist 1", "Artist 2"]
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.ARTISTS_NAMES: None}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_preserves_other_fields(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"],
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ALBUM_NAME: "Test Album"
        })
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: None})
        
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) is None
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Test Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_delete_artists_already_none(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) is None

    def test_delete_artists_empty_list(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: []})
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.ARTISTS_NAMES: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) is None
