"""Tests for language metadata."""

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
from audiometa.utils.AppMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestLanguageMetadata:
    """Test cases for language metadata."""

    def test_language_metadata_mp3(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test language metadata in MP3 file."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.LANGUAGE: "en"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == "en"

    def test_language_metadata_flac(self, sample_flac_file: Path, temp_audio_file: Path):
        """Test language metadata in FLAC file."""
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.LANGUAGE: "en"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        language = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == "en"

    def test_language_metadata_wav(self, sample_wav_file: Path, temp_audio_file: Path):
        """Test language metadata in WAV file (may not be supported)."""
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        test_metadata = {UnifiedMetadataKey.LANGUAGE: "en"}
        update_file_metadata(temp_audio_file, test_metadata)
        
        # WAV files may not support language metadata
        metadata = get_merged_app_metadata(temp_audio_file)
        assert UnifiedMetadataKey.LANGUAGE not in metadata or metadata.get(UnifiedMetadataKey.LANGUAGE) is None

    def test_language_metadata_with_audio_file_object(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test language metadata using AudioFile object."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        audio_file = AudioFile(temp_audio_file)
        test_metadata = {UnifiedMetadataKey.LANGUAGE: "en"}
        update_file_metadata(audio_file, test_metadata)
        
        language = get_specific_metadata(audio_file, UnifiedMetadataKey.LANGUAGE)
        assert language == "en"

    def test_language_metadata_edge_cases(self, sample_mp3_file: Path, temp_audio_file: Path):
        """Test language metadata with edge cases."""
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Test different language codes
        test_languages = ["en", "es", "fr", "de", "ja"]
        for lang in test_languages:
            test_metadata = {UnifiedMetadataKey.LANGUAGE: lang}
            update_file_metadata(temp_audio_file, test_metadata)
            
            retrieved_lang = get_specific_metadata(temp_audio_file, UnifiedMetadataKey.LANGUAGE)
            assert retrieved_lang == lang

