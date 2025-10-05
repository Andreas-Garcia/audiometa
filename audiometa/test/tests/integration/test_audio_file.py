"""Integration tests for AudioFile class with metadata APIs."""

import pytest
from pathlib import Path

from audiometa import (
    AudioFile,
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata
)
from audiometa.utils.MetadataSingleFormat import MetadataSingleFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.integration
class TestAudioFileIntegration:
    """Integration test cases for AudioFile class with metadata APIs."""


    def test_audio_file_object_integration(self, sample_mp3_file: Path):
        """Test integration between AudioFile object and functional APIs."""
        audio_file = AudioFile(sample_mp3_file)
        
        # Test that AudioFile object works with functional APIs
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)
        
        # Test single format with AudioFile object
        id3v2_metadata = get_single_format_app_metadata(audio_file, MetadataSingleFormat.ID3V2)
        assert isinstance(id3v2_metadata, dict)
        
        # Test specific metadata with AudioFile object
        title = get_specific_metadata(audio_file, AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)



