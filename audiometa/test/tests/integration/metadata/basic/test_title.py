"""Tests for title metadata."""

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
class TestTitleMetadata:
    """Test cases for title metadata."""

    def test_title_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test writing title
        test_metadata = {UnifiedMetadataKey.TITLE: "Test Song Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Test reading title
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == "Test Song Title"
        
        # Test reading from merged metadata
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Song Title"

    def test_title_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.TITLE: "FLAC Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == "FLAC Test Title"

    def test_title_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.TITLE: "WAV Test Title"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        title = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TITLE)
        assert title == "WAV Test Title"

    def test_title_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.TITLE: "AudioFile Test Title"}
        update_file_metadata(audio_file, test_metadata)
        
        title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
        assert title == "AudioFile Test Title"

    def test_title_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test short title
        short_title = "A"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: short_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == short_title
        
        # Test long title
        long_title = "A" * 1000
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: long_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) is not None
        assert len(metadata.get(UnifiedMetadataKey.TITLE)) > 0
        
        # Test empty title
        empty_title = ""
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: empty_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == empty_title

    def test_title_metadata_reading(self, metadata_id3v1_small_mp3, metadata_id3v2_small_mp3, metadata_riff_small_wav, metadata_vorbis_small_flac):
        # ID3v1 title (limited to 30 characters)
        metadata = get_merged_unified_metadata(metadata_id3v1_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) == 30  # ID3v1 limit
        
        # ID3v2 title (can be longer)
        metadata = get_merged_unified_metadata(metadata_id3v2_small_mp3)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # ID3v2 can have longer titles
        
        # RIFF title (can be longer)
        metadata = get_merged_unified_metadata(metadata_riff_small_wav)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # RIFF can have longer titles
        
        # Vorbis title (can be very long)
        metadata = get_merged_unified_metadata(metadata_vorbis_small_flac)
        title = metadata.get(UnifiedMetadataKey.TITLE)
        assert isinstance(title, str)
        assert len(title) > 30  # Vorbis can have very long titles

    def test_title_metadata_writing(self, metadata_none_mp3, metadata_none_flac, metadata_none_wav, temp_audio_file):
        # Test MP3
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_title = "Test Title MP3"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: test_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == test_title
        
        # Test FLAC
        shutil.copy2(metadata_none_flac, temp_audio_file)
        test_title = "Test Title FLAC"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: test_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == test_title
        
        # Test WAV
        shutil.copy2(metadata_none_wav, temp_audio_file)
        test_title = "Test Title WAV"
        update_file_metadata(temp_audio_file, {UnifiedMetadataKey.TITLE: test_title})
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert metadata.get(UnifiedMetadataKey.TITLE) == test_title

