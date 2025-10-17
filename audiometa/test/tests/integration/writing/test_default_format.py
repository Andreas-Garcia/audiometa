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

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_merged_unified_metadata
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestDefaultWritingFormat:

    def test_mp3_default_writes_to_id3v2(self):
        # Prepare test metadata
        test_metadata = {
            UnifiedMetadataKey.TITLE: "MP3 Test Title",
            UnifiedMetadataKey.ARTISTS_NAMES: ["MP3 Test Artist"],
            UnifiedMetadataKey.ALBUM_NAME: "MP3 Test Album",
            UnifiedMetadataKey.BPM: 120
        }
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Update metadata using default format (should be ID3v2)
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify metadata was written to ID3v2 format
            id3v2_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "MP3 Test Title"
            assert id3v2_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["MP3 Test Artist"]
            assert id3v2_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "MP3 Test Album"
            assert id3v2_metadata.get(UnifiedMetadataKey.BPM) == 120
        
            # Verify that merged metadata (which follows priority order) returns ID3v2 data
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "MP3 Test Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["MP3 Test Artist"]

    def test_mp3_default_writes_to_id3v2_3_version(self):
        from mutagen.id3 import ID3
        
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Prepare test metadata
            test_metadata = {
                UnifiedMetadataKey.TITLE: "MP3 Default Version Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["MP3 Default Version Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "MP3 Default Version Test Album"
            }
            
            # Update metadata using default format (should be ID3v2.3)
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify that the file now contains ID3v2.3 tags (default version)
            id3_tags = ID3(test_file.path)
            assert id3_tags.version == (2, 3, 0), f"Expected ID3v2.3 as default, but got version {id3_tags.version}"

    def test_flac_default_writes_to_vorbis(self):
        with TempFileWithMetadata({}, "flac") as test_file:
            # Prepare test metadata
            test_metadata = {
                UnifiedMetadataKey.TITLE: "FLAC Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["FLAC Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "FLAC Test Album",
                UnifiedMetadataKey.BPM: 140
            }
            
            # Update metadata using default format (should be Vorbis)
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify metadata was written to Vorbis format
            vorbis_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.VORBIS)
            assert vorbis_metadata.get(UnifiedMetadataKey.TITLE) == "FLAC Test Title"
            assert vorbis_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["FLAC Test Artist"]
            assert vorbis_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "FLAC Test Album"
            assert vorbis_metadata.get(UnifiedMetadataKey.BPM) == 140
            
            # Verify that merged metadata (which follows priority order) returns Vorbis data
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "FLAC Test Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["FLAC Test Artist"]

    def test_wav_default_writes_to_riff(self):
        with TempFileWithMetadata({}, "wav") as test_file:
            # Prepare test metadata (RIFF has limited support, so we test supported fields)
            test_metadata = {
                UnifiedMetadataKey.TITLE: "WAV Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["WAV Test Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "WAV Test Album",
                UnifiedMetadataKey.GENRES_NAMES: "Test Genre"
            }
            
            # Update metadata using default format (should be RIFF)
            update_file_metadata(test_file.path, test_metadata)
            
            # Verify metadata was written to RIFF format
            riff_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.RIFF)
            assert riff_metadata.get(UnifiedMetadataKey.TITLE) == "WAV Test Title"
            assert riff_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["WAV Test Artist"]
            assert riff_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "WAV Test Album"
            assert riff_metadata.get(UnifiedMetadataKey.GENRES_NAMES) == "Other"
            
            # Verify that merged metadata (which follows priority order) returns RIFF data
            merged_metadata = get_merged_unified_metadata(test_file.path)
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

    def test_default_format_consistency_across_audio_types(self):
        test_cases = [
            ("mp3", MetadataFormat.ID3V2, "MP3"),
            ("flac", MetadataFormat.VORBIS, "FLAC"),
            ("wav", MetadataFormat.RIFF, "WAV")
        ]
        
        for format_type, expected_format, file_type in test_cases:
            with TempFileWithMetadata({}, format_type) as test_file:
                # Test metadata
                test_metadata = {
                    UnifiedMetadataKey.TITLE: f"{file_type} Default Test",
                    UnifiedMetadataKey.ARTISTS_NAMES: [f"{file_type} Artist"]
                }
                
                # Write using default format
                update_file_metadata(test_file.path, test_metadata)
                
                # Verify it was written to the expected default format
                default_metadata = get_single_format_app_metadata(test_file.path, expected_format)
                assert default_metadata.get(UnifiedMetadataKey.TITLE) == f"{file_type} Default Test"
                assert default_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == [f"{file_type} Artist"]

    def test_id3v1_writing_support(self):
        with TempFileWithMetadata({}, "id3v1") as test_file:
            # Test writing directly to ID3v1 format
            test_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v1 Test Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v1 Test Artist"]
            }
            
            # Write directly to ID3v1 format
            update_file_metadata(test_file.path, test_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Verify ID3v1 was written
            id3v1_metadata = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v1_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v1 Test Title"
            assert id3v1_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["ID3v1 Test Artist"]
        
        # Test default behavior still uses ID3v2 as primary format
        test_metadata2 = {
            UnifiedMetadataKey.TITLE: "ID3v2 Test Title"
        }
        update_file_metadata(temp_audio_file, test_metadata2)
        
        # Verify ID3v2 was written (default behavior)
        id3v2_metadata = get_single_format_app_metadata(temp_audio_file, MetadataFormat.ID3V2)
        assert id3v2_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2 Test Title"

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
