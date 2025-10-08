"""Tests for writing title metadata using external scripts.

This refactored version uses external scripts instead of the app's
update functions to prevent circular dependencies in tests.
"""

import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.test_script_helpers import create_test_file_with_specific_metadata


@pytest.mark.integration
class TestTitleWriting:
    def test_mp3(self, metadata_none_mp3, temp_audio_file):
        test_title = "Test Title MP3"
        test_metadata = {"title": test_title}
        
        # Use external script to set metadata instead of app's update function
        create_test_file_with_specific_metadata(
            metadata_none_mp3, 
            temp_audio_file, 
            test_metadata, 
            "mp3"
        )
        
        # Now test that our reading logic works correctly
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title

    def test_wav(self, metadata_none_wav, temp_audio_file):
        test_title = "Test Title WAV"
        test_metadata = {"title": test_title}
        
        # Use external script to set metadata instead of app's update function
        create_test_file_with_specific_metadata(
            metadata_none_wav, 
            temp_audio_file, 
            test_metadata, 
            "wav"
        )
        
        # Now test that our reading logic works correctly
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title

    def test_flac(self, metadata_none_flac, temp_audio_file):
        test_title = "Test Title FLAC"
        test_metadata = {"title": test_title}
        
        # Use external script to set metadata instead of app's update function
        create_test_file_with_specific_metadata(
            metadata_none_flac, 
            temp_audio_file, 
            test_metadata, 
            "flac"
        )
        
        # Now test that our reading logic works correctly
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == test_title