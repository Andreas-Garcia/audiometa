"""Tests for PRESERVE metadata writing strategy.

This module tests the PRESERVE strategy which writes to native format only
and preserves existing metadata in other formats.
"""

import pytest
from pathlib import Path

from audiometa import update_metadata, get_unified_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.MetadataWritingStrategy import MetadataWritingStrategy
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestPreserveStrategy:

    def test_preserve_strategy_wav_with_id3v2(self, sample_wav_file: Path, temp_audio_file: Path):
        # First, add ID3v2 metadata using external script
        id3v2_metadata = {
            "title": "ID3v2 Title",
            "artist": "ID3v2 Artist",
            "album": "ID3v2 Album"
        }
        
        with TempFileWithMetadata(id3v2_metadata, "wav") as test_file:
            # Set ID3v2 metadata using helper method
            test_file.set_id3v2_title("ID3v2 Title")
            test_file.set_id3v2_artist("ID3v2 Artist")
            test_file.set_id3v2_album("ID3v2 Album")
            
            # Verify ID3v2 metadata was written
            id3v2_result = get_unified_metadata(test_file, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_result.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Now write RIFF metadata with PRESERVE strategy (default)
            # This part still uses the app's function since we're testing the strategy
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            update_metadata(test_file, riff_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Verify both formats exist
            id3v2_after = get_unified_metadata(test_file, metadata_format=MetadataFormat.ID3V2)
            riff_after = get_unified_metadata(test_file, metadata_format=MetadataFormat.RIFF)
            
            # ID3v2 should be preserved (unchanged)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            # RIFF should have new metadata
            assert riff_after.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            
            # Merged metadata should prefer RIFF (WAV native format has higher precedence)
            merged = get_unified_metadata(test_file)
            assert merged.get(UnifiedMetadataKey.TITLE) == "RIFF Title"

    def test_id3v1_not_preserved_with_preserve_strategy(self):
        # Create test file with ID3v1 metadata using external script
        with TempFileWithMetadata({}, "mp3") as test_file:
            # Add ID3v1 metadata using helper method
            test_file.set_id3v1_title("ID3v1 Title")
            test_file.set_id3v1_artist("ID3v1 Artist")
            test_file.set_id3v1_album("ID3v1 Album")
            
            # Verify ID3v1 metadata was written
            id3v1_result = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_result.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"
            
            # Now write ID3v2 metadata with PRESERVE strategy
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            update_metadata(test_file.path, id3v2_metadata, metadata_strategy=MetadataWritingStrategy.PRESERVE)
            
            # Verify ID3v1 metadata behavior with PRESERVE strategy
            # ID3v1 should be preserved (not overwritten) with PRESERVE strategy
            id3v1_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V1)
            assert id3v1_after.get(UnifiedMetadataKey.TITLE) == "ID3v1 Title"  # ID3v1 was preserved
            
            # Verify ID3v2 metadata was written
            id3v2_after = get_unified_metadata(test_file.path, metadata_format=MetadataFormat.ID3V2)
            assert id3v2_after.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Merged metadata should prefer ID3v2 (higher precedence)
            merged = get_unified_metadata(test_file.path)
            assert merged.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
