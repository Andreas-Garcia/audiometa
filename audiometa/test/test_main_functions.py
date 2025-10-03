"""Tests for main module functions."""

import pytest
from pathlib import Path
import tempfile
import shutil

from audiometa import (
    get_bitrate,
    get_duration_in_sec,
    is_flac_md5_valid,
    fix_md5_checking,
    delete_potential_id3_metadata_with_header
)
from audiometa.exceptions import FileTypeNotSupportedError


class TestMainFunctions:
    """Test cases for main module functions."""

    def test_get_bitrate_mp3(self, sample_mp3_file: Path):
        """Test getting bitrate from MP3 file."""
        bitrate = get_bitrate(sample_mp3_file)
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_flac(self, sample_flac_file: Path):
        """Test getting bitrate from FLAC file."""
        bitrate = get_bitrate(sample_flac_file)
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_wav(self, sample_wav_file: Path):
        """Test getting bitrate from WAV file."""
        bitrate = get_bitrate(sample_wav_file)
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_with_audio_file_object(self, sample_mp3_file: Path):
        """Test getting bitrate using AudioFile object."""
        from audiometa import AudioFile
        audio_file = AudioFile(sample_mp3_file)
        bitrate = get_bitrate(audio_file)
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_duration_in_sec_mp3(self, sample_mp3_file: Path):
        """Test getting duration from MP3 file."""
        duration = get_duration_in_sec(sample_mp3_file)
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_flac(self, sample_flac_file: Path):
        """Test getting duration from FLAC file."""
        duration = get_duration_in_sec(sample_flac_file)
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_wav(self, sample_wav_file: Path):
        """Test getting duration from WAV file."""
        duration = get_duration_in_sec(sample_wav_file)
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_with_audio_file_object(self, sample_mp3_file: Path):
        """Test getting duration using AudioFile object."""
        from audiometa import AudioFile
        audio_file = AudioFile(sample_mp3_file)
        duration = get_duration_in_sec(audio_file)
        assert isinstance(duration, float)
        assert duration > 0

    def test_is_flac_md5_valid_flac(self, sample_flac_file: Path):
        """Test FLAC MD5 validation on FLAC file."""
        is_valid = is_flac_md5_valid(sample_flac_file)
        assert isinstance(is_valid, bool)

    def test_is_flac_md5_valid_non_flac(self, sample_mp3_file: Path):
        """Test FLAC MD5 validation on non-FLAC file raises error."""
        with pytest.raises(FileTypeNotSupportedError):
            is_flac_md5_valid(sample_mp3_file)

    def test_is_flac_md5_valid_with_audio_file_object(self, sample_flac_file: Path):
        """Test FLAC MD5 validation using AudioFile object."""
        from audiometa import AudioFile
        audio_file = AudioFile(sample_flac_file)
        is_valid = is_flac_md5_valid(audio_file)
        assert isinstance(is_valid, bool)

    def test_fix_md5_checking_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test fixing MD5 checking for FLAC file."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # Fix MD5 checking
        fixed_file_path = fix_md5_checking(temp_audio_file)
        assert isinstance(fixed_file_path, str)
        assert Path(fixed_file_path).exists()
        
        # Clean up
        Path(fixed_file_path).unlink()

    def test_fix_md5_checking_non_flac(self, sample_mp3_file: Path):
        """Test fixing MD5 checking on non-FLAC file raises error."""
        with pytest.raises(FileTypeNotSupportedError):
            fix_md5_checking(sample_mp3_file)

    def test_fix_md5_checking_with_audio_file_object(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test fixing MD5 checking using AudioFile object."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        from audiometa import AudioFile
        audio_file = AudioFile(temp_audio_file)
        
        # Fix MD5 checking
        fixed_file_path = fix_md5_checking(audio_file)
        assert isinstance(fixed_file_path, str)
        assert Path(fixed_file_path).exists()
        
        # Clean up
        Path(fixed_file_path).unlink()

    def test_delete_potential_id3_metadata_with_header_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting ID3 metadata from MP3 file."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(temp_audio_file)

    def test_delete_potential_id3_metadata_with_header_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test deleting ID3 metadata from FLAC file."""
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(temp_audio_file)

    def test_delete_potential_id3_metadata_with_header_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test deleting ID3 metadata using AudioFile object."""
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        from audiometa import AudioFile
        audio_file = AudioFile(temp_audio_file)
        
        # This should not raise an error
        delete_potential_id3_metadata_with_header(audio_file)

    def test_unsupported_file_type_raises_error(self, temp_audio_file: Path):
        """Test that unsupported file types raise FileTypeNotSupportedError."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_bitrate(str(temp_audio_file))
        
        with pytest.raises(FileTypeNotSupportedError):
            get_duration_in_sec(str(temp_audio_file))



