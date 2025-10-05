"""Tests for BPM metadata."""

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
class TestBpmMetadata:
    """Test cases for BPM metadata."""

    def test_bpm_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test BPM metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.BPM: 128}
        update_file_metadata(temp_audio_file, test_metadata)
        
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm == 128

    def test_bpm_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test BPM metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.BPM: 128}
        update_file_metadata(temp_audio_file, test_metadata)
        
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm == 128

    def test_bpm_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test BPM metadata in WAV file (may not be supported)."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.BPM: 120}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # WAV files may not support BPM metadata
        metadata = get_merged_unified_metadata(temp_audio_file)
        assert UnifiedMetadataKey.BPM not in metadata or metadata.get(UnifiedMetadataKey.BPM) is None

    def test_bpm_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test BPM metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.BPM: 128}
        update_file_metadata(audio_file, test_metadata)
        
        bpm = get_specific_metadata(audio_file, UnifiedMetadataKey.BPM)
        assert bpm == 128

    def test_bpm_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test BPM metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different BPM values
        test_bpms = [60, 120, 140, 200]
        for bpm in test_bpms:
            test_metadata = {UnifiedMetadataKey.BPM: bpm}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
            assert retrieved_bpm == bpm

