"""Tests for title metadata."""

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
from audiometa.utils.AppMetadataKey import AppMetadataKey


@pytest.mark.integration
class TestTitleMetadata:
    """Test cases for title metadata."""

    def test_title_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test title metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test writing title
        test_metadata = {AppMetadataKey.TITLE: "Test Song Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Test reading title
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "Test Song Title"
        
        # Test reading from merged metadata
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == "Test Song Title"

    def test_title_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test title metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.TITLE: "FLAC Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "FLAC Test Title"

    def test_title_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test title metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.TITLE: "WAV Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, AppMetadataKey.TITLE)
        assert title == "WAV Test Title"

    def test_title_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test title metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {AppMetadataKey.TITLE: "AudioFile Test Title"}
        update_file_metadata(audio_file, test_metadata)
        
        title = get_specific_metadata(audio_file, AppMetadataKey.TITLE)
        assert title == "AudioFile Test Title"

    def test_title_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test title metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test short title
        short_title = "A"
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: short_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == short_title
        
        # Test long title
        long_title = "A" * 1000
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: long_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) is not None
        assert len(metadata.get(AppMetadataKey.TITLE)) > 0
        
        # Test empty title
        empty_title = ""
        update_file_metadata(temp_audio_file, {AppMetadataKey.TITLE: empty_title})
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.TITLE) == empty_title

