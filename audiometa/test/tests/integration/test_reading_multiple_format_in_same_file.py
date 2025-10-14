"""Tests for reading multiple metadata formats in the same file using external scripts.

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.

This module tests scenarios where multiple metadata formats exist in the same file
and verifies that the correct precedence rules are applied.
"""

import pytest
from pathlib import Path

from audiometa import (
    get_merged_unified_metadata,
    get_single_format_app_metadata,
    get_specific_metadata,
    update_file_metadata,
    AudioFile
)
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata


@pytest.mark.integration
class TestConflictingMetadata:

    def test_id3v1_vs_id3v2_precedence_mp3(self, metadata_id3v1_and_id3v2_mp3):
        # This test uses a pre-existing file with both ID3v1 and ID3v2 metadata
        
        # Merged metadata should prefer ID3v2
        merged_metadata = get_merged_unified_metadata(metadata_id3v1_and_id3v2_mp3)
        assert merged_metadata.get(UnifiedMetadataKey.TITLE) is not None
        assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) is not None
        assert merged_metadata.get(UnifiedMetadataKey.ALBUM_NAME) is not None
        
        # Individual format extraction should work
        id3v1_data = get_single_format_app_metadata(metadata_id3v1_and_id3v2_mp3, MetadataFormat.ID3V1)
        id3v2_data = get_single_format_app_metadata(metadata_id3v1_and_id3v2_mp3, MetadataFormat.ID3V2)
        
        # Both formats should have data
        assert id3v1_data.get(UnifiedMetadataKey.TITLE) is not None
        assert id3v2_data.get(UnifiedMetadataKey.TITLE) is not None
        
        # ID3v2 should take precedence in merged metadata
        assert merged_metadata.get(UnifiedMetadataKey.TITLE) == id3v2_data.get(UnifiedMetadataKey.TITLE)

    def test_id3v2_vs_riff_precedence_wav(self, sample_wav_file: Path, temp_wav_file: Path):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "wav") as test_file:
            # Set different values in RIFF and ID3v2 using app's functions (this is what we're testing)
            riff_metadata = {
                UnifiedMetadataKey.TITLE: "RIFF Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["RIFF Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "RIFF Album"
            }
            
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            
            # Write RIFF first, then ID3v2
            update_file_metadata(test_file.path, riff_metadata, metadata_format=MetadataFormat.RIFF)
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Merged metadata should prefer RIFF (WAV native format)
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "RIFF Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["RIFF Artist"]
            assert merged_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "RIFF Album"

    def test_vorbis_vs_id3v2_precedence_flac(self, sample_flac_file: Path, test_file: Path):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "flac") as test_file:
            # Set different values in ID3v2 and Vorbis using app's functions (this is what we're testing)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["ID3v2 Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            
            vorbis_metadata = {
                UnifiedMetadataKey.TITLE: "Vorbis Title",
                UnifiedMetadataKey.ARTISTS_NAMES: ["Vorbis Artist"],
                UnifiedMetadataKey.ALBUM_NAME: "Vorbis Album"
            }
            
            # Write ID3v2 first, then Vorbis
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            update_file_metadata(test_file.path, vorbis_metadata, metadata_format=MetadataFormat.VORBIS)
            
            # Merged metadata should prefer Vorbis
            merged_metadata = get_merged_unified_metadata(test_file.path)
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "Vorbis Title"
            assert merged_metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Vorbis Artist"]
            assert merged_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Vorbis Album"

    def test_partial_conflicts(self):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Add both ID3v1 and ID3v2 metadata for testing
            id3v1_metadata = {
                "title": "ID3v1 Title",
                "artist": "ID3v1 Artist",
                "album": "ID3v1 Album",
                "year": "2023",
                "genre": "Rock"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            id3v2_metadata = {
                UnifiedMetadataKey.TITLE: "ID3v2 Title",
                UnifiedMetadataKey.ALBUM_NAME: "ID3v2 Album"
            }
            
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            merged_metadata = get_merged_unified_metadata(test_file.path)
            
            # Title should come from ID3v2
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            # Album should come from ID3v2
            assert merged_metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "ID3v2 Album"

    def test_rating_precedence_rules(self):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Add ID3v1 metadata first
            id3v1_metadata = {
                "title": "ID3v1 Title",
                "artist": "ID3v1 Artist",
                "album": "ID3v1 Album",
                "year": "2023",
                "genre": "Rock"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            
            # Test ID3v2 rating precedence
            id3v2_metadata = {UnifiedMetadataKey.RATING: 5}
            
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            merged_metadata = get_merged_unified_metadata(test_file.path)
            
            # Should use ID3v2 rating
            assert merged_metadata.get(UnifiedMetadataKey.RATING) == 5

    def test_audio_file_object_with_conflicts(self):
        # Use external script to set initial metadata
        initial_metadata = {
            "title": "Original Title",
            "artist": "Original Artist"
        }
        
        with TempFileWithMetadata(initial_metadata, "mp3") as test_file:
            # Add both ID3v1 and ID3v2 metadata for testing
            id3v1_metadata = {
                "title": "ID3v1 Title",
                "artist": "ID3v1 Artist",
                "album": "ID3v1 Album",
                "year": "2023",
                "genre": "Rock"
            }
            update_file_metadata(test_file.path, id3v1_metadata, metadata_format=MetadataFormat.ID3V1)
            id3v2_metadata = {UnifiedMetadataKey.TITLE: "ID3v2 Title"}
            
            update_file_metadata(test_file.path, id3v2_metadata, metadata_format=MetadataFormat.ID3V2)
            
            # Test with AudioFile object
            audio_file = AudioFile(test_file.path)
            merged_metadata = get_merged_unified_metadata(audio_file)
            
            assert merged_metadata.get(UnifiedMetadataKey.TITLE) == "ID3v2 Title"
            
            # Test specific metadata extraction
            title = get_specific_metadata(audio_file, UnifiedMetadataKey.TITLE)
            assert title == "ID3v2 Title"