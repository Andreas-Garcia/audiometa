"""Tests for FLAC MD5-related functions."""

import pytest
from pathlib import Path
import shutil

from audiometa import is_flac_md5_valid, fix_md5_checking
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.unit
class TestFlacMd5Functions:
    """Test cases for FLAC MD5-related functions."""

    def test_is_flac_md5_valid_flac(self, sample_flac_file: Path):
        is_valid = is_flac_md5_valid(sample_flac_file)
        assert isinstance(is_valid, bool)

    def test_is_flac_md5_valid_non_flac(self, sample_mp3_file: Path):
        """Test FLAC MD5 validation on non-FLAC file raises error."""
        with pytest.raises(FileTypeNotSupportedError):
            is_flac_md5_valid(sample_mp3_file)

    def test_is_flac_md5_valid_with_audio_file_object(self, sample_flac_file: Path):
        from audiometa import AudioFile
        audio_file = AudioFile(sample_flac_file)
        is_valid = is_flac_md5_valid(audio_file)
        assert isinstance(is_valid, bool)

    def test_fix_md5_checking_flac(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        # Fix MD5 checking
        fixed_file_path = fix_md5_checking(temp_flac_file)
        assert isinstance(fixed_file_path, str)
        assert Path(fixed_file_path).exists()
        
        # Clean up
        Path(fixed_file_path).unlink()

    def test_fix_md5_checking_non_flac(self, sample_mp3_file: Path):
        """Test fixing MD5 checking on non-FLAC file raises error."""
        with pytest.raises(FileTypeNotSupportedError):
            fix_md5_checking(sample_mp3_file)

    def test_fix_md5_checking_with_audio_file_object(self, sample_flac_file: Path, temp_flac_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_flac_file)
        
        from audiometa import AudioFile
        audio_file = AudioFile(temp_flac_file)
        
        # Fix MD5 checking
        fixed_file_path = fix_md5_checking(audio_file)
        assert isinstance(fixed_file_path, str)
        assert Path(fixed_file_path).exists()
        
        # Clean up
        Path(fixed_file_path).unlink()
