"""Tests for additional metadata fields (composer, publisher, copyright, lyrics, etc.)."""

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
from audiometa.utils.TagFormat import MetadataFormat


class TestAdditionalMetadata:
    """Test cases for additional metadata fields."""

    def test_composer_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test composer metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COMPOSER: "Test Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPOSER)
        assert composer == "Test Composer"

    def test_composer_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test composer metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COMPOSER: "FLAC Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPOSER)
        assert composer == "FLAC Composer"

    def test_composer_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test composer metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COMPOSER: "WAV Composer"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        composer = get_specific_metadata(temp_audio_file, AppMetadataKey.COMPOSER)
        assert composer == "WAV Composer"

    def test_publisher_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test publisher metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.PUBLISHER: "Test Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        publisher = get_specific_metadata(temp_audio_file, AppMetadataKey.PUBLISHER)
        assert publisher == "Test Publisher"

    def test_publisher_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test publisher metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.PUBLISHER: "FLAC Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        publisher = get_specific_metadata(temp_audio_file, AppMetadataKey.PUBLISHER)
        assert publisher == "FLAC Publisher"

    def test_publisher_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that publisher is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support publisher, so this should be ignored
        test_metadata = {AppMetadataKey.PUBLISHER: "WAV Publisher"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Publisher should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.PUBLISHER not in metadata or metadata.get(AppMetadataKey.PUBLISHER) is None

    def test_copyright_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test copyright metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COPYRIGHT: "© 2024 Test Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, AppMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 Test Label"

    def test_copyright_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test copyright metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COPYRIGHT: "© 2024 FLAC Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, AppMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 FLAC Label"

    def test_copyright_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test copyright metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.COPYRIGHT: "© 2024 WAV Label"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        copyright_info = get_specific_metadata(temp_audio_file, AppMetadataKey.COPYRIGHT)
        assert copyright_info == "© 2024 WAV Label"

    def test_lyrics_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test lyrics metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_lyrics = "These are the test lyrics\nFor the test song\nWith multiple lines"
        test_metadata = {AppMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        
        lyrics = get_specific_metadata(temp_audio_file, AppMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test lyrics metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_lyrics = "FLAC test lyrics\nWith multiple lines\nAnd special characters: àéîôù"
        test_metadata = {AppMetadataKey.LYRICS: test_lyrics}
        update_file_metadata(temp_audio_file, test_metadata)
        
        lyrics = get_specific_metadata(temp_audio_file, AppMetadataKey.LYRICS)
        assert lyrics == test_lyrics

    def test_lyrics_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that lyrics is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support lyrics, so this should be ignored
        test_metadata = {AppMetadataKey.LYRICS: "WAV test lyrics"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Lyrics should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.LYRICS not in metadata or metadata.get(AppMetadataKey.LYRICS) is None

    def test_comment_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test comment metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_comment = "This is a test comment with special characters: àéîôù"
        test_metadata = {AppMetadataKey.COMMENT: test_comment}
        update_file_metadata(temp_audio_file, test_metadata)
        
        comment = get_specific_metadata(temp_audio_file, AppMetadataKey.COMMENT)
        assert comment == test_comment

    def test_comment_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test comment metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_comment = "FLAC test comment"
        test_metadata = {AppMetadataKey.COMMENT: test_comment}
        update_file_metadata(temp_audio_file, test_metadata)
        
        comment = get_specific_metadata(temp_audio_file, AppMetadataKey.COMMENT)
        assert comment == test_comment

    def test_comment_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test comment metadata in WAV file."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_comment = "WAV test comment"
        test_metadata = {AppMetadataKey.COMMENT: test_comment}
        update_file_metadata(temp_audio_file, test_metadata)
        
        comment = get_specific_metadata(temp_audio_file, AppMetadataKey.COMMENT)
        assert comment == test_comment

    def test_encoder_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test encoder metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ENCODER: "LAME 3.100"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        encoder = get_specific_metadata(temp_audio_file, AppMetadataKey.ENCODER)
        assert encoder == "LAME 3.100"

    def test_encoder_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test encoder metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {AppMetadataKey.ENCODER: "FLAC 1.4.2"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        encoder = get_specific_metadata(temp_audio_file, AppMetadataKey.ENCODER)
        assert encoder == "FLAC 1.4.2"

    def test_url_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test URL metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_url = "https://example.com/track/123"
        test_metadata = {AppMetadataKey.URL: test_url}
        update_file_metadata(temp_audio_file, test_metadata)
        
        url = get_specific_metadata(temp_audio_file, AppMetadataKey.URL)
        assert url == test_url

    def test_url_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test URL metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_url = "https://example.com/flac/456"
        test_metadata = {AppMetadataKey.URL: test_url}
        update_file_metadata(temp_audio_file, test_metadata)
        
        url = get_specific_metadata(temp_audio_file, AppMetadataKey.URL)
        assert url == test_url

    def test_url_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that URL is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support URL, so this should be ignored
        test_metadata = {AppMetadataKey.URL: "https://example.com/wav/789"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # URL should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.URL not in metadata or metadata.get(AppMetadataKey.URL) is None

    def test_isrc_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test ISRC metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_isrc = "USRC17607839"
        test_metadata = {AppMetadataKey.ISRC: test_isrc}
        update_file_metadata(temp_audio_file, test_metadata)
        
        isrc = get_specific_metadata(temp_audio_file, AppMetadataKey.ISRC)
        assert isrc == test_isrc

    def test_isrc_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test ISRC metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_isrc = "GBUM71500678"
        test_metadata = {AppMetadataKey.ISRC: test_isrc}
        update_file_metadata(temp_audio_file, test_metadata)
        
        isrc = get_specific_metadata(temp_audio_file, AppMetadataKey.ISRC)
        assert isrc == test_isrc

    def test_isrc_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that ISRC is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support ISRC, so this should be ignored
        test_metadata = {AppMetadataKey.ISRC: "FRZ038190174"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # ISRC should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.ISRC not in metadata or metadata.get(AppMetadataKey.ISRC) is None

    def test_mood_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test mood metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_mood = "Happy"
        test_metadata = {AppMetadataKey.MOOD: test_mood}
        update_file_metadata(temp_audio_file, test_metadata)
        
        mood = get_specific_metadata(temp_audio_file, AppMetadataKey.MOOD)
        assert mood == test_mood

    def test_mood_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test mood metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_mood = "Melancholic"
        test_metadata = {AppMetadataKey.MOOD: test_mood}
        update_file_metadata(temp_audio_file, test_metadata)
        
        mood = get_specific_metadata(temp_audio_file, AppMetadataKey.MOOD)
        assert mood == test_mood

    def test_mood_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that mood is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support mood, so this should be ignored
        test_metadata = {AppMetadataKey.MOOD: "Energetic"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Mood should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.MOOD not in metadata or metadata.get(AppMetadataKey.MOOD) is None

    def test_key_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test key metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_key = "C"
        test_metadata = {AppMetadataKey.KEY: test_key}
        update_file_metadata(temp_audio_file, test_metadata)
        
        key = get_specific_metadata(temp_audio_file, AppMetadataKey.KEY)
        assert key == test_key

    def test_key_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test key metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_key = "Am"
        test_metadata = {AppMetadataKey.KEY: test_key}
        update_file_metadata(temp_audio_file, test_metadata)
        
        key = get_specific_metadata(temp_audio_file, AppMetadataKey.KEY)
        assert key == test_key

    def test_key_metadata_wav_not_supported(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test that key is not supported in WAV files."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # WAV files don't support key, so this should be ignored
        test_metadata = {AppMetadataKey.KEY: "G"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Key should not be present for WAV files
        metadata = get_merged_app_metadata(temp_audio_file)
        assert AppMetadataKey.KEY not in metadata or metadata.get(AppMetadataKey.KEY) is None

    def test_complete_additional_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test all additional metadata fields together in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {
            AppMetadataKey.COMPOSER: "Test Composer",
            AppMetadataKey.PUBLISHER: "Test Publisher",
            AppMetadataKey.COPYRIGHT: "© 2024 Test Label",
            AppMetadataKey.LYRICS: "Test lyrics\nWith multiple lines",
            AppMetadataKey.COMMENT: "Test comment",
            AppMetadataKey.ENCODER: "LAME 3.100",
            AppMetadataKey.URL: "https://example.com/track",
            AppMetadataKey.ISRC: "USRC17607839",
            AppMetadataKey.MOOD: "Happy",
            AppMetadataKey.KEY: "C"
        }
        
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify all fields
        metadata = get_merged_app_metadata(temp_audio_file)
        assert metadata.get(AppMetadataKey.COMPOSER) == "Test Composer"
        assert metadata.get(AppMetadataKey.PUBLISHER) == "Test Publisher"
        assert metadata.get(AppMetadataKey.COPYRIGHT) == "© 2024 Test Label"
        assert metadata.get(AppMetadataKey.LYRICS) == "Test lyrics\nWith multiple lines"
        assert metadata.get(AppMetadataKey.COMMENT) == "Test comment"
        assert metadata.get(AppMetadataKey.ENCODER) == "LAME 3.100"
        assert metadata.get(AppMetadataKey.URL) == "https://example.com/track"
        assert metadata.get(AppMetadataKey.ISRC) == "USRC17607839"
        assert metadata.get(AppMetadataKey.MOOD) == "Happy"
        assert metadata.get(AppMetadataKey.KEY) == "C"

    def test_additional_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test additional metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {
            AppMetadataKey.COMPOSER: "AudioFile Composer",
            AppMetadataKey.PUBLISHER: "AudioFile Publisher",
            AppMetadataKey.COMMENT: "AudioFile Comment"
        }
        
        update_file_metadata(audio_file, test_metadata)
        
        metadata = get_merged_app_metadata(audio_file)
        assert metadata.get(AppMetadataKey.COMPOSER) == "AudioFile Composer"
        assert metadata.get(AppMetadataKey.PUBLISHER) == "AudioFile Publisher"
        assert metadata.get(AppMetadataKey.COMMENT) == "AudioFile Comment"

    def test_empty_additional_metadata_handling(self, sample_mp3_file: Path):
        """Test handling of empty or missing additional metadata."""
        # Test reading from file with no additional metadata
        metadata = get_merged_app_metadata(sample_mp3_file)
        assert isinstance(metadata, dict)
        
        # Test getting specific additional metadata that doesn't exist
        composer = get_specific_metadata(sample_mp3_file, AppMetadataKey.COMPOSER)
        assert composer is None or isinstance(composer, str)
        
        publisher = get_specific_metadata(sample_mp3_file, AppMetadataKey.PUBLISHER)
        assert publisher is None or isinstance(publisher, str)
        
        lyrics = get_specific_metadata(sample_mp3_file, AppMetadataKey.LYRICS)
        assert lyrics is None or isinstance(lyrics, str)



