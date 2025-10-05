"""Tests for ID3v1 metadata manager."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.id3v1.Id3v1Manager import Id3v1Manager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.unit
class TestId3v1Manager:
    """Test cases for ID3v1 metadata manager."""

    def test_id3v1_manager_mp3(self, sample_mp3_file: Path):
        """Test ID3v1 manager with MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_flac(self, sample_flac_file: Path):
        """Test ID3v1 manager with FLAC file (may have ID3v1 tags)."""
        audio_file = AudioFile(sample_flac_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_get_specific_metadata(self, sample_mp3_file: Path):
        """Test getting specific metadata from ID3v1 manager."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        title = manager.get_app_specific_metadata(UnifiedMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_id3v1_manager_update_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata with ID3v1 manager."""
        import shutil
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = Id3v1Manager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v1 Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "ID3v1 Test Album"
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v1 Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v1 Test Album"
