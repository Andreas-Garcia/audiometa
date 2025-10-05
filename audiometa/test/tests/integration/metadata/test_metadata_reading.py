"""Tests for metadata reading functionality."""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_app_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    AudioFile
)
from audiometa.utils.MetadataSingleFormat import MetadataSingleFormat
from audiometa.utils.AppMetadataKey import AppMetadataKey
from audiometa.exceptions import FileTypeNotSupportedError


@pytest.mark.integration
class TestMetadataReading:
    """Test cases for metadata reading functionality."""

    def test_get_merged_app_metadata_mp3(self, sample_mp3_file: Path):
        """Test getting merged metadata from MP3 file."""
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        # Should contain some basic metadata fields
        assert any(key in metadata for key in [
            AppMetadataKey.TITLE,
            AppMetadataKey.ARTISTS_NAMES,
            AppMetadataKey.ALBUM_NAME
        ])

    def test_get_merged_app_metadata_flac(self, sample_flac_file: Path):
        """Test getting merged metadata from FLAC file."""
        metadata = get_merged_app_metadata(sample_flac_file)
        assert isinstance(metadata, dict)

    def test_get_merged_app_metadata_wav(self, sample_wav_file: Path):
        """Test getting merged metadata from WAV file."""
        metadata = get_merged_app_metadata(sample_wav_file)
        assert isinstance(metadata, dict)

    def test_get_merged_app_metadata_with_audio_file_object(self, sample_mp3_file: Path):
        """Test getting merged metadata using AudioFile object."""
        audio_file = AudioFile(sample_mp3_file)
        metadata = get_merged_app_metadata(audio_file)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_id3v2(self, sample_mp3_file: Path):
        """Test getting ID3v2 metadata from MP3 file."""
        metadata = get_single_format_app_metadata(sample_mp3_file, MetadataSingleFormat.ID3V2)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_vorbis(self, sample_flac_file: Path):
        """Test getting Vorbis metadata from FLAC file."""
        metadata = get_single_format_app_metadata(sample_flac_file, MetadataSingleFormat.VORBIS)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_riff(self, sample_wav_file: Path):
        """Test getting RIFF metadata from WAV file."""
        metadata = get_single_format_app_metadata(sample_wav_file, MetadataSingleFormat.RIFF)
        assert isinstance(metadata, dict)

    def test_get_single_format_app_metadata_unsupported_format(self, sample_mp3_file: Path):
        """Test getting metadata with unsupported format raises error."""
        with pytest.raises(FileTypeNotSupportedError):
            get_single_format_app_metadata(sample_mp3_file, MetadataSingleFormat.VORBIS)

    def test_get_specific_metadata_title(self, sample_mp3_file: Path):
        """Test getting specific title metadata."""
        title = get_specific_metadata(sample_mp3_file, AppMetadataKey.TITLE)
        # Title might be None if not present, but should not raise error
        assert title is None or isinstance(title, str)

    def test_get_specific_metadata_artists(self, sample_mp3_file: Path):
        """Test getting specific artists metadata."""
        artists = get_specific_metadata(sample_mp3_file, AppMetadataKey.ARTISTS_NAMES)
        # Artists might be None if not present, but should not raise error
        assert artists is None or isinstance(artists, list)

    def test_get_specific_metadata_rating(self, sample_mp3_file: Path):
        """Test getting specific rating metadata."""
        rating = get_specific_metadata(sample_mp3_file, AppMetadataKey.RATING)
        # Rating might be None if not present, but should not raise error
        assert rating is None or isinstance(rating, (int, float))

    def test_get_specific_metadata_with_audio_file_object(self, sample_mp3_file: Path):
        """Test getting specific metadata using AudioFile object."""
        audio_file = AudioFile(sample_mp3_file)
        title = get_specific_metadata(audio_file, AppMetadataKey.TITLE)
        assert title is None or isinstance(title, str)

    def test_metadata_with_normalized_rating(self, sample_mp3_file: Path):
        """Test metadata reading with normalized rating."""
        metadata = get_merged_app_metadata(sample_mp3_file, normalized_rating_max_value=100)
        assert isinstance(metadata, dict)

    def test_metadata_with_different_rating_normalization(self, sample_mp3_file: Path):
        """Test metadata reading with different rating normalization."""
        metadata = get_merged_app_metadata(sample_mp3_file, normalized_rating_max_value=255)
        assert isinstance(metadata, dict)

    def test_unsupported_file_type_raises_error(self, temp_audio_file: Path):
        """Test that unsupported file types raise FileTypeNotSupportedError."""
        # Create a file with unsupported extension
        temp_audio_file.write_bytes(b"fake audio content")
        temp_audio_file = temp_audio_file.with_suffix(".txt")
        temp_audio_file.write_bytes(b"fake audio content")
        
        with pytest.raises(FileTypeNotSupportedError):
            get_merged_app_metadata(str(temp_audio_file))



