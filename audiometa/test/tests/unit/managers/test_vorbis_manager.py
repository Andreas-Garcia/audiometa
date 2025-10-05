"""Tests for Vorbis metadata manager."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.rating_supporting.VorbisManager import VorbisManager
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.unit
class TestVorbisManager:
    """Test cases for Vorbis metadata manager."""

    def test_vorbis_manager_flac(self, sample_flac_file: Path):
        """Test Vorbis manager with FLAC file."""
        audio_file = AudioFile(sample_flac_file)
        manager = VorbisManager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_vorbis_manager_ogg(self, sample_ogg_file: Path):
        """Test Vorbis manager with OGG file."""
        audio_file = AudioFile(sample_ogg_file)
        manager = VorbisManager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_vorbis_manager_with_rating_normalization(self, sample_flac_file: Path):
        """Test Vorbis manager with rating normalization."""
        audio_file = AudioFile(sample_flac_file)
        manager = VorbisManager(audio_file, normalized_rating_max_value=100)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_vorbis_manager_update_metadata(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test updating metadata with Vorbis manager."""
        import shutil
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = VorbisManager(audio_file)
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "Vorbis Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["Vorbis Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "Vorbis Test Album",
            UnifiedMetadataKey.RATING: 75,
            UnifiedMetadataKey.BPM: 140
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(UnifiedMetadataKey.TITLE) == "Vorbis Test Title"
        assert updated_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Vorbis Test Artist"]
        assert updated_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Vorbis Test Album"
        assert updated_metadata.get(UnifiedMetadataKey.RATING) == 75
        assert updated_metadata.get(UnifiedMetadataKey.BPM) == 140
