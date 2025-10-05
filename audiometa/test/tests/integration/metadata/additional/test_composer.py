"""Tests for composer metadata."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_app_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestComposerMetadata:
    """Test cases for composer metadata."""

    def test_composer_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test composer metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COMPOSER: "Test Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == "Test Composer"

    def test_composer_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test composer metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COMPOSER: "FLAC Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == "FLAC Composer"

    def test_composer_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test composer metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COMPOSER: "WAV Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == "WAV Composer"

    def test_composer_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test composer metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.COMPOSER: "AudioFile Composer"}
        update_file_metadata(audio_file, test_metadata)
        
        composer = get_specific_metadata(audio_file, UnifiedMetadataKey.COMPOSER)
        assert composer == "AudioFile Composer"

