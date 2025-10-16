import pytest
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestRatingDeleting:
    def test_delete_rating_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: 50}, metadata_format=MetadataFormat.ID3V2, normalized_rating_max_value=100)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) == 50
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: None}, metadata_format=MetadataFormat.ID3V2)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None

    def test_delete_rating_id3v1(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: 50}, metadata_format=MetadataFormat.ID3V1, normalized_rating_max_value=100)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) == 50
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: None}, metadata_format=MetadataFormat.ID3V1)
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None

    def test_delete_rating_riff(self, metadata_none_wav, temp_wav_file):
        shutil.copy2(metadata_none_wav, temp_wav_file)
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.RATING: 50}, metadata_format=MetadataFormat.RIFF, normalized_rating_max_value=100)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) == 50
        
        update_file_metadata(temp_wav_file, {UnifiedMetadataKey.RATING: None}, metadata_format=MetadataFormat.RIFF)
        assert get_specific_metadata(temp_wav_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None

    def test_delete_rating_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.RATING: 50}, metadata_format=MetadataFormat.VORBIS, normalized_rating_max_value=100)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) == 50
        
        update_file_metadata(temp_flac_file, {UnifiedMetadataKey.RATING: None}, metadata_format=MetadataFormat.VORBIS)
        assert get_specific_metadata(temp_flac_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None

    def test_delete_rating_preserves_other_fields(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {
            UnifiedMetadataKey.RATING: 75,
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Test Artist"]
        }, normalized_rating_max_value=100)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: None})
        
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE) == "Test Title"
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]

    def test_delete_rating_already_none(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None

    def test_delete_rating_zero(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: 0}, normalized_rating_max_value=100)
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.RATING: None})
        assert get_specific_metadata(temp_audio_file, UnifiedMetadataKey.RATING, normalized_rating_max_value=100) is None
