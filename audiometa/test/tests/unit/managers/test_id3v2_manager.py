"""Tests for ID3v2 metadata manager."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.rating_supporting.Id3v2Manager import Id3v2Manager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.unit
class TestId3v2Manager:
    """Test cases for ID3v2 metadata manager."""

    def test_id3v2_manager_mp3(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v2Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_wav(self, sample_wav_file: Path):
        audio_file = AudioFile(sample_wav_file)
        manager = Id3v2Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_with_rating_normalization(self, sample_mp3_file: Path):
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v2Manager(audio_file, normalized_rating_max_value=100)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_update_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata with ID3v2 manager."""
        import shutil
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = Id3v2Manager(audio_file, normalized_rating_max_value=100)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v2 Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Test Album",
            UnifiedMetadataKey.RATING: 80,
            UnifiedMetadataKey.BPM: 120
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2 Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v2 Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2 Test Album"
        assert updated_metadata.get(UnifiedMetadataKey.RATING) == 80
        assert updated_metadata.get(UnifiedMetadataKey.BPM) == 120
