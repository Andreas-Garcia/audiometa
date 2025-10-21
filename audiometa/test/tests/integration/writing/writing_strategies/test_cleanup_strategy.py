"""Tests for CLEANUP metadata writing strategy.

This module tests the CLEANUP strategy which writes to native format
and removes all non-native metadata formats.
"""

import pytest
from pathlib import Path

from audiometa import (
    update_file_metadata,
    get_single_format_app_metadata,
    get_unified_metadata,
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestCleanupStrategy:

    def test_cleanup_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # Create test file with basic metadata first
        basic_metadata = {
            "title": "Basic Title",
            "artist": "Basic Artist",
            "album": "Basic Album"
        }
        
        with TempFileWithMetadata(basic_metadata, "wav") as test_file:
            # First, add ID3v2 metadata using TempFileWithMetadata
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            test_file.set_id3v2_album("ID3v2 Album")
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Now write RIFF metadata with CLEANUP strategy
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            update_file_metadata(test_file, riff_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
            
            # Verify ID3v2 was removed
            id3v2_after = get_single_format_app_metadata(test_file, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) is None
            
            # Verify RIFF has new metadata
            riff_after = get_single_format_app_metadata(test_file, MetadataFormat.RIFF)
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should only have RIFF (ID3v2 was cleaned up)
            merged = get_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_not_preserved_with_cleanup_strategy(self):
        # Create test file with ID3v1 metadata using external script
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v1 metadata using TempFileWithMetadata
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v1_album("ID3v1 Album")
            
            # Verify ID3v1 metadata was written
            id3v1_result = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Now write ID3v2 metadata with CLEANUP strategy
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            update_file_metadata(test_file.path, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.CLEANUP)
            
            # Verify ID3v1 metadata behavior with CLEANUP strategy
            # ID3v1 should be removed (cleaned up) with CLEANUP strategy
            id3v1_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) is None  # ID3v1 was cleaned up
            
            # Verify ID3v2 metadata was written
            id3v2_after = get_single_format_app_metadata(test_file.path, MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Merged metadata should prefer ID3v2 (higher precedence)
            merged = get_unified_metadata(test_file.path)
            assert merged.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
