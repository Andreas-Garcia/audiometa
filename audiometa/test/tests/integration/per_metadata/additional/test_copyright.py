"""Tests for copyright metadata."""

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
class TestCopyrightMetadata:
    """Test cases for copyright metadata."""

    def test_copyright_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test copyright metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: "© 2024 Test Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 Test Label"

    def test_copyright_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test copyright metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: "© 2024 FLAC Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 FLAC Label"

    def test_copyright_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test copyright metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: "© 2024 WAV Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 WAV Label"

    def test_copyright_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test copyright metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.COPYRIGHT: "© 2024 AudioFile Label"}
        update_file_metadata(audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(audio_file, UnifiedMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 AudioFile Label"

