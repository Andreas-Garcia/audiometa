"""Tests for writing BPM metadata."""

import pytest
from pathlib import Path
import shutil

from audiometa import get_specific_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat


@pytest.mark.integration
class TestBpmWriting:
    def test_id3v2(self, metadata_none_mp3, temp_audio_file):
        shutil.copy2(metadata_none_mp3, temp_audio_file)
        test_bpm = 128
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        update_file_metadata(temp_audio_file, test_metadata, metadata_format=MetadataFormat.ID3V2)
        bpm = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.BPM)
        assert bpm == test_bpm

    def test_riff(self, metadata_none_wav, temp_wav_file):
        """Test that RIFF format correctly raises exception for unsupported BPM metadata."""
        from audiometa.exceptions import MetadataNotSupportedError
        
        shutil.copy2(metadata_none_wav, temp_wav_file)
        test_bpm = 120
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        
        # RIFF format raises exception for unsupported metadata
        with pytest.raises(MetadataNotSupportedError, match="UnifiedMetadataKey.BPM metadata not supported by RIFF format"):
            update_file_metadata(temp_wav_file, test_metadata, metadata_format=MetadataFormat.RIFF)

    def test_vorbis(self, metadata_none_flac, temp_flac_file):
        shutil.copy2(metadata_none_flac, temp_flac_file)
        test_bpm = 140
        test_metadata = {UnifiedMetadataKey.BPM: test_bpm}
        update_file_metadata(temp_flac_file, test_metadata, metadata_format=MetadataFormat.VORBIS)
        bpm = get_specific_metadata(temp_flac_file, UnifiedMetadataKey.BPM)
        assert bpm == test_bpm
