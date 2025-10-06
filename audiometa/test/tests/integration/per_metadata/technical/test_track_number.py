"""Tests for track number metadata."""

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
class TestTrackNumberMetadata:
    """Test cases for track number metadata."""

    def test_track_number_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test track number metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: 7}
        update_file_metadata(temp_audio_file, test_metadata)
        
        track = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track == 7

    def test_track_number_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test track number metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: 7}
        update_file_metadata(temp_audio_file, test_metadata)
        
        track = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track == 7

    def test_track_number_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test track number metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: 7}
        update_file_metadata(temp_audio_file, test_metadata)
        
        track = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track == 7

    def test_track_number_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test track number metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: 7}
        update_file_metadata(audio_file, test_metadata)
        
        track = get_specific_metadata(audio_file, UnifiedMetadataKey.TRACK_NUMBER)
        assert track == 7

    def test_track_number_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test track number metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different track numbers
        test_tracks = [1, 5, 10, 99, 999]
        for track in test_tracks:
            test_metadata = {UnifiedMetadataKey.TRACK_NUMBER: track}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_track = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.TRACK_NUMBER)
            assert retrieved_track == track

