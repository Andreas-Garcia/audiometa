import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestTrackNumberDeleting:
    def test_delete_track_number_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: 5}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) == 5
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: None}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) is None

    def test_delete_track_number_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: 3}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) == 3
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: None}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) is None

    def test_delete_track_number_preserves_other_fields(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {
            UnifiedMetadataKey.TRACK_NUMBER: 7,
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
        })
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: None})
        
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) is None
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Test Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_track_number_already_none(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) is None

    def test_delete_track_number_zero(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: 0})
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TRACK_NUMBER: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER) is None
