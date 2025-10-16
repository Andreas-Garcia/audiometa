import pytest
from pathlib import Path

from audiometa import get_merged_unified_metadata, update_file_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


class TestSmartParsingScenarios:
    """
    Test the smart parsing scenarios described in the README:
    
    - Modern formats (ID3v2, Vorbis) + Multiple entries: No separator parsing
    - Modern formats (ID3v2, Vorbis) + Single entry: Applies separator parsing  
    - Legacy formats (RIFF, ID3v1): Always applies separator parsing
    """

    def test_scenario_1_modern_format_multiple_entries_no_parsing_id3v2(self):
        """Scenario 1: ID3v2 uses single frame with separators - gets parsed on read"""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set multiple separate artist entries (ID3v2 will concatenate them)
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist; with; semicolons", "Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # ID3v2 stores as single frame with separators, so it gets parsed on read
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One/Artist" in artists
            assert "with" in artists
            assert "semicolons/Artist Three" in artists

    def test_scenario_1_modern_format_multiple_entries_no_parsing_vorbis(self):
        """Scenario 1: Modern file with separate entries - separators preserved (Vorbis)"""
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set multiple separate artist entries (modern format)
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist; with; semicolons", "Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should preserve separators in individual entries (no parsing)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist; with; semicolons" in artists  # Separators preserved
            assert "Artist Three" in artists

    def test_scenario_2_legacy_data_modern_format_single_entry_parsed_id3v2(self):
        """Scenario 2: Legacy data in modern format - single entry gets parsed (ID3v2)"""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set single artist entry with semicolons (legacy data in modern format)
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two;Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should parse single entry with separators
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_scenario_2_legacy_data_modern_format_single_entry_parsed_vorbis(self):
        """Scenario 2: Legacy data in modern format - single entry gets parsed (Vorbis)"""
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # Set single artist entry with semicolons (legacy data in modern format)
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two;Artist Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should parse single entry with separators
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_scenario_3_legacy_format_always_parses_riff(self):
        """Scenario 3: Legacy format (RIFF) - always applies separator parsing"""
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            # Set single artist entry with semicolons in RIFF format
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.RIFF)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should always parse in legacy format
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists

    def test_scenario_3_legacy_format_always_parses_id3v1(self):
        """Scenario 3: Legacy format (ID3v1) - always applies separator parsing"""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set single artist entry with semicolons in ID3v1 format
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One;Artist Two"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            
            # Should always parse in legacy format
            assert isinstance(artists, list)
            assert len(artists) == 2
            assert "Artist One" in artists
            assert "Artist Two" in artists

    def test_mixed_scenario_modern_format_with_both_patterns(self):
        """Test mixed scenario: ID3v2 concatenates multiple entries, single entries get parsed"""
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # Set artists as multiple separate entries (ID3v2 will concatenate them)
            # Set composers as single entry with separators (should parse)
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist; with; semicolons", "Artist Three"],
                UnifiedMetadataKey.COMPOSER: ["Composer One;Composer Two;Composer Three"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Read metadata
            unified_metadata = get_merged_unified_metadata(test_file.path)
            
            # Artists get concatenated by ID3v2, then parsed on read
            artists = unified_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One/Artist" in artists
            assert "with" in artists
            assert "semicolons/Artist Three" in artists
            
            # Composers should parse separators (single entry)
            composers = unified_metadata.get(UnifiedMetadataKey.COMPOSER)
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "Composer One" in composers
            assert "Composer Two" in composers
            assert "Composer Three" in composers
