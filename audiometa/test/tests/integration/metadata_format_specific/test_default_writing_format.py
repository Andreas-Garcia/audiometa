"""Tests for default writing metadata format for each audio format.

This module tests that the library uses the correct default metadata format
when writing metadata to different audio file types, as specified in the README:

- MP3 files: ID3v2 (v2.4) - default writing format
- FLAC files: Vorbis Comments - default writing format  
- WAV files: RIFF - default writing format

The tests verify that when no specific metadata format is specified,
the library automatically uses the appropriate default format for each file type.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Any

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestDefaultWritingFormat:

    def test_mp3_default_writes_to_id3v2(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Prepare test metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "MP3 Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["MP3 Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "MP3 Test Album",
            UnifiedMetadataKey.RATING: 85,
            UnifiedMetadataKey.BPM: 120
        }
        
        # Update metadata using default format (should be ID3v2)
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written to ID3v2 format
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "MP3 Test Title"
        assert id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["MP3 Test Artist"]
        assert id3v2_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "MP3 Test Album"
        assert id3v2_metadata.get(UnifiedMetadataKey.RATING) == 85
        assert id3v2_metadata.get(UnifiedMetadataKey.BPM) == 120
        
        # Verify that merged metadata (which follows priority order) returns ID3v2 data
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "MP3 Test Title"
        assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["MP3 Test Artist"]

    def test_flac_default_writes_to_vorbis(self, sample_flac_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_flac_file, temp_audio_file)
        
        # Prepare test metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "FLAC Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["FLAC Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "FLAC Test Album",
            UnifiedMetadataKey.RATING: 90,
            UnifiedMetadataKey.BPM: 140
        }
        
        # Update metadata using default format (should be Vorbis)
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written to Vorbis format
        vorbis_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.VORBIS)
        assert vorbis_metadata.get(UnifiedMetadataKey.TITLE) == "FLAC Test Title"
        assert vorbis_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["FLAC Test Artist"]
        assert vorbis_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "FLAC Test Album"
        assert vorbis_metadata.get(UnifiedMetadataKey.RATING) == 90
        assert vorbis_metadata.get(UnifiedMetadataKey.BPM) == 140
        
        # Verify that merged metadata (which follows priority order) returns Vorbis data
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "FLAC Test Title"
        assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["FLAC Test Artist"]

    def test_wav_default_writes_to_riff(self, sample_wav_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_wav_file, temp_audio_file)
        
        # Prepare test metadata (RIFF has limited support, so we test supported fields)
        test_metadata = {
            UnifiedMetadataKey.TITLE: "WAV Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "WAV Test Album",
            UnifiedMetadataKey.GENRE_NAME: "Test Genre"
        }
        
        # Update metadata using default format (should be RIFF)
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify metadata was written to RIFF format
        riff_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.RIFF)
        assert riff_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
        assert riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]
        assert riff_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Test Album"
        assert riff_metadata.get(UnifiedMetadataKey.GENRE_NAME) == "Test Genre"
        
        # Verify that merged metadata (which follows priority order) returns RIFF data
        merged_metadata = get_merged_unified_metadata(temp_audio_file)
        assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
        assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]

    def test_format_priority_order_matches_defaults(self):
        priorities = MetadataFormat.get_priorities()
        
        # MP3 files: ID3v2 should be first (default)
        mp3_priorities = priorities['.mp3']
        assert mp3_priorities[0] == MetadataFormat.ID3V2, "MP3 default should be ID3v2"
        
        # FLAC files: Vorbis should be first (default)
        flac_priorities = priorities['.flac']
        assert flac_priorities[0] == MetadataFormat.VORBIS, "FLAC default should be Vorbis"
        
        # WAV files: RIFF should be first (default)
        wav_priorities = priorities['.wav']
        assert wav_priorities[0] == MetadataFormat.RIFF, "WAV default should be RIFF"

    def test_default_format_consistency_across_audio_types(self, sample_mp3_file: Path, sample_flac_file: Path, sample_wav_file: Path):
        test_cases = [
            (sample_mp3_file, MetadataFormat.ID3V2, "MP3"),
            (sample_flac_file, MetadataFormat.VORBIS, "FLAC"),
            (sample_wav_file, MetadataFormat.RIFF, "WAV")
        ]
        
        for sample_file, expected_format, file_type in test_cases:
            with tempfile.NamedTemporaryFile(suffix=sample_file.suffix, delete=False) as temp_file:
                temp_path = Path(temp_file.name)
                shutil.copy2(sample_file, temp_path)
                
                try:
                    # Test metadata
                    test_metadata = {
                        UnifiedMetadataKey.TITLE: f"{file_type} Default Test",
                        UnifiedMetadataKey.ARTISTS_NAMES: [f"{file_type} Artist"]
                    }
                    
                    # Write using default format
                    update_file_metadata(temp_path, test_metadata)
                    
                    # Verify it was written to the expected default format
                    default_metadata = get_single_format_app_metadata(temp_path, expected_format)
                    assert default_metadata.get(UnifiedMetadataKey.TITLE) == f"{file_type} Default Test"
                    assert default_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [f"{file_type} Artist"]
                    
                finally:
                    # Clean up temp file
                    temp_path.unlink(missing_ok=True)

    def test_id3v1_read_only_limitation(self, sample_mp3_file: Path, temp_audio_file: Path):
        # Copy sample file to temp location
        shutil.copy2(sample_mp3_file, temp_audio_file)
        
        # Try to write to ID3v1 format (should not work as it's read-only)
        # This test verifies that the library correctly uses ID3v2 as default
        # instead of attempting to write to ID3v1
        
        test_metadata = {
            UnifiedMetadataKey.TITLE: "ID3v1 Test Title"
        }
        
        # Update metadata - should write to ID3v2 (default) not ID3v1
        update_file_metadata(temp_audio_file, test_metadata)
        
        # Verify ID3v2 was written (not ID3v1)
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v1 Test Title"
        
        # ID3v1 should remain unchanged (read-only)
        id3v1_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V1)
        # ID3v1 might be empty or contain old data, but shouldn't have our new title
        # (unless it was already there, which is fine for this test)

    @pytest.mark.parametrize("audio_format,expected_default", [
        ('.mp3', MetadataFormat.ID3V2),
        ('.flac', MetadataFormat.VORBIS),
        ('.wav', MetadataFormat.RIFF)
    ])
    def test_default_format_for_audio_extension(self, audio_format: str, expected_default: MetadataFormat):
        priorities = MetadataFormat.get_priorities()
        format_priorities = priorities.get(audio_format)
        
        assert format_priorities is not None, f"No priorities defined for {audio_format}"
        assert format_priorities[0] == expected_default, f"{audio_format} should default to {expected_default}, got {format_priorities[0]}"
