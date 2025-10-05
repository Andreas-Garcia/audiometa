"""Tests for AudioFile class."""

import pytest
from pathlib import Path

from audiometa import AudioFile
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestAudioFile:
    """Test cases for AudioFile class."""

    def test_audio_file_with_string_path(self, sample_mp3_file: Path):
        """Test AudioFile initialization with string path."""
        audio_file = AudioFile(str(sample_mp3_file))
        assert audio_file.file_path == str(sample_mp3_file)
        assert audio_file.file_extension == ".mp3"

    def test_audio_file_with_path_object(self, sample_mp3_file: Path):
        """Test AudioFile initialization with Path object."""
        audio_file = AudioFile(sample_mp3_file)
        assert audio_file.file_path == str(sample_mp3_file)
        assert audio_file.file_extension == ".mp3"

    def test_audio_file_nonexistent_file(self):
        """Test AudioFile with non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            AudioFile("nonexistent_file.mp3")

    def test_audio_file_unsupported_type(self, temp_audio_file: Path):
        """Test AudioFile with unsupported file type."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            AudioFile(str(temp_audio_file))

    def test_get_duration_in_sec_mp3(self, sample_mp3_file: Path):
        """Test getting duration for MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_flac(self, sample_flac_file: Path):
        """Test getting duration for FLAC file."""
        audio_file = AudioFile(sample_flac_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_duration_in_sec_wav(self, sample_wav_file: Path):
        """Test getting duration for WAV file."""
        audio_file = AudioFile(sample_wav_file)
        duration = audio_file.get_duration_in_sec()
        assert isinstance(duration, float)
        assert duration > 0

    def test_get_bitrate_mp3(self, sample_mp3_file: Path):
        """Test getting bitrate for MP3 file."""
        audio_file = AudioFile(sample_mp3_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_flac(self, sample_flac_file: Path):
        """Test getting bitrate for FLAC file."""
        audio_file = AudioFile(sample_flac_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_get_bitrate_wav(self, sample_wav_file: Path):
        """Test getting bitrate for WAV file."""
        audio_file = AudioFile(sample_wav_file)
        bitrate = audio_file.get_bitrate()
        assert isinstance(bitrate, int)
        assert bitrate > 0

    def test_file_operations(self, temp_audio_file: Path):
        """Test file read/write operations."""
        audio_file = AudioFile(temp_audio_file)
        
        # Test write
        test_data = b"test audio data"
        bytes_written = audio_file.write(test_data)
        assert bytes_written == len(test_data)
        
        # Test read
        read_data = audio_file.read()
        assert read_data == test_data

    def test_file_name_methods(self, sample_mp3_file: Path):
        """Test file name methods."""
        audio_file = AudioFile(sample_mp3_file)
        
        # Test system filename
        system_name = audio_file.get_file_name_system()
        assert system_name == sample_mp3_file.name
        
        # Test original filename (should be same as system for string paths)
        original_name = audio_file.get_file_name_original()
        assert original_name == sample_mp3_file.name

    def test_flac_md5_validation(self, sample_flac_file: Path):
        """Test FLAC MD5 validation."""
        audio_file = AudioFile(sample_flac_file)
        
        # This should not raise an exception
        is_valid = audio_file.is_flac_file_md5_valid()
        assert isinstance(is_valid, bool)

    def test_flac_md5_validation_non_flac(self, sample_mp3_file: Path):
        """Test FLAC MD5 validation on non-FLAC file raises error."""
        audio_file = AudioFile(sample_mp3_file)
        
        with pytest.raises(FileTypeNotSupportedError):
            audio_file.is_flac_file_md5_valid()

    def test_context_manager(self, sample_mp3_file: Path):
        """Test AudioFile as context manager."""
        with AudioFile(sample_mp3_file) as audio_file:
            assert audio_file.file_path == str(sample_mp3_file)
            # Context manager should work without issues



