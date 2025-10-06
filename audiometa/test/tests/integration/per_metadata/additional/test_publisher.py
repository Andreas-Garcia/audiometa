"""Tests for publisher metadata."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_merged_unified_metadata,
    update_file_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestPublisherMetadata:

    def test_publisher_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "Test Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "Test Publisher"

    def test_publisher_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test publisher metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "FLAC Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "FLAC Publisher"

    def test_publisher_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test publisher metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "WAV Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # WAV files support publisher metadata through ID3v2 tags
        publisher = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "WAV Publisher"

    def test_publisher_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.PUBLISHER: "AudioFile Publisher"}
        update_file_metadata(audio_file, test_metadata)
        
        publisher = get_specific_metadata(audio_file, UnifiedMetadataKey.PUBLISHER)
        assert publisher == "AudioFile Publisher"

