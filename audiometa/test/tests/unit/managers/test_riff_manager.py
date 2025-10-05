"""Tests for RIFF metadata manager."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.rating_supporting.RiffManager import RiffManager
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.unit
class TestRiffManager:
    """Test cases for RIFF metadata manager."""

    def test_riff_manager_wav(self, sample_wav_file: Path):
        """Test RIFF manager with WAV file."""
        audio_file = AudioFile(sample_wav_file)
        manager = RiffManager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_riff_manager_unsupported_format(self, sample_mp3_file: Path):
        """Test RIFF manager with unsupported format raises error."""
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            RiffManager(audio_file)

    def test_riff_manager_update_metadata(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test updating metadata with RIFF manager."""
        import shutil
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = RiffManager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "RIFF Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "RIFF Test Album"
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "RIFF Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["RIFF Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "RIFF Test Album"

    def test_riff_manager_rating_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that RIFF manager doesn't support rating."""
        import shutil
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = RiffManager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "RIFF Test Title",
            UnifiedMetadataKey.RATING: 85  # RIFF doesn't support rating
        }
        
        # This should not raise an error, but rating should be ignored
        manager.update_file_metadata(test_metadata)
        
        # Verify only supported metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "RIFF Test Title"
        # Rating should not be present for RIFF files
        assert UnifiedMetadataKey.RATING not in updated_metadata
