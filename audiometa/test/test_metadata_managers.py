"""Tests for metadata manager classes."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.manager.id3v1.Id3v1Manager import Id3v1Manager
from audiometa.manager.rating_supporting.Id3v2Manager import Id3v2Manager
from audiometa.manager.rating_supporting.VorbisManager import VorbisManager
from audiometa.manager.rating_supporting.RiffManager import RiffManager
from audiometa.utils.TagFormat import MetadataFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


class TestId3v1Manager:
    """Test cases for ID3v1 metadata manager."""

    def test_id3v1_manager_mp3(self, sample_mp3_file: Path):
        """Test ID3v1 manager with MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v1_manager_unsupported_format(self, sample_flac_file: Path):
        """Test ID3v1 manager with unsupported format raises error."""
        audio_file = AudioFile(sample_flac_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            Id3v1Manager(audio_file)

    def test_id3v1_manager_get_specific_metadata(self, sample_mp3_file: Path):
        """Test getting specific metadata from ID3v1 manager."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v1Manager(audio_file)
        
        title = manager.get_app_specific_metadata(AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_id3v1_manager_update_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata with ID3v1 manager."""
        import shutil
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = Id3v1Manager(audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "ID3v1 Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["ID3v1 Test Artist"],
            AppMetadataKey.ALBUM_NAME: "ID3v1 Test Album"
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(AppMetadataKey.TITLE) == "ID3v1 Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["ID3v1 Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "ID3v1 Test Album"


class TestId3v2Manager:
    """Test cases for ID3v2 metadata manager."""

    def test_id3v2_manager_mp3(self, sample_mp3_file: Path):
        """Test ID3v2 manager with MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v2Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_wav(self, sample_wav_file: Path):
        """Test ID3v2 manager with WAV file."""
        audio_file = AudioFile(sample_wav_file)
        manager = Id3v2Manager(audio_file)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_with_rating_normalization(self, sample_mp3_file: Path):
        """Test ID3v2 manager with rating normalization."""
        audio_file = AudioFile(sample_mp3_file)
        manager = Id3v2Manager(audio_file, normalized_rating_max_value=100)
        
        metadata = manager.get_app_metadata()
        assert isinstance(metadata, dict)

    def test_id3v2_manager_update_metadata(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test updating metadata with ID3v2 manager."""
        import shutil
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = Id3v2Manager(audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "ID3v2 Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["ID3v2 Test Artist"],
            AppMetadataKey.ALBUM_NAME: "ID3v2 Test Album",
            AppMetadataKey.RATING: 85,
            AppMetadataKey.BPM: 120
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(AppMetadataKey.TITLE) == "ID3v2 Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["ID3v2 Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "ID3v2 Test Album"
        assert updated_metadata.get(AppMetadataKey.RATING) == 85
        assert updated_metadata.get(AppMetadataKey.BPM) == 120


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
            AppMetadataKey.TITLE: "Vorbis Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["Vorbis Test Artist"],
            AppMetadataKey.ALBUM_NAME: "Vorbis Test Album",
            AppMetadataKey.RATING: 75,
            AppMetadataKey.BPM: 140
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(AppMetadataKey.TITLE) == "Vorbis Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["Vorbis Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "Vorbis Test Album"
        assert updated_metadata.get(AppMetadataKey.RATING) == 75
        assert updated_metadata.get(AppMetadataKey.BPM) == 140


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
            AppMetadataKey.TITLE: "RIFF Test Title",
            AppMetadataKey.ARTISTS_NAMES: ["RIFF Test Artist"],
            AppMetadataKey.ALBUM_NAME: "RIFF Test Album"
        }
        
        manager.update_file_metadata(test_metadata)
        
        # Verify metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(AppMetadataKey.TITLE) == "RIFF Test Title"
        assert updated_metadata.get(AppMetadataKey.ARTISTS_NAMES) == ["RIFF Test Artist"]
        assert updated_metadata.get(AppMetadataKey.ALBUM_NAME) == "RIFF Test Album"

    def test_riff_manager_rating_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that RIFF manager doesn't support rating."""
        import shutil
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        manager = RiffManager(audio_file)
        
        test_metadata = {
            AppMetadataKey.TITLE: "RIFF Test Title",
            AppMetadataKey.RATING: 85  # RIFF doesn't support rating
        }
        
        # This should not raise an error, but rating should be ignored
        manager.update_file_metadata(test_metadata)
        
        # Verify only supported metadata was updated
        updated_metadata = manager.get_app_metadata()
        assert updated_metadata.get(AppMetadataKey.TITLE) == "RIFF Test Title"
        # Rating should not be present for RIFF files
        assert AppMetadataKey.RATING not in updated_metadata



