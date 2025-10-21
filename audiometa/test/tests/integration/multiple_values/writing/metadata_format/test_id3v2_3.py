from pathlib import Path

from audiometa import update_file_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_inspector import ID3v2MetadataInspector
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter


class TestMultipleEntriesId3v2_3:
        
    def test_artists_concatenation(self):
        initial_metadata = {"title": "Test Song"}
        with TempFileWithMetadata(initial_metadata, "id3v2.3") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist 1", "Artist 2", "Artist 3"]
            }
            
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            # Use helper to check the created ID3v2 frame directly
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            assert verification['success']
            
            # Check that all artists are concatenated with separators in ID3v2.3
            raw_output = verification['raw_output']
            assert "TPE1=Artist 1//Artist 2//Artist 3" in raw_output
    
    def test_with_existing_artists_field(self):
        # Start with an existing artist field
        initial_metadata = {"artist": "Existing Artist"}
        with TempFileWithMetadata(initial_metadata, "id3v2.3") as test_file:
            ID3v2MetadataSetter.set_artist(test_file.path, "Existing 1; Existing 2", version="2.3")
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            raw_output = verification['raw_output']
            assert "TPE1=Existing 1; Existing 2" in raw_output
            
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Existing 1", "New 2"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 3, 0))
            
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            assert verification['success']
            raw_output = verification['raw_output']
            assert "Existing 1" in raw_output
            assert "New 2" in raw_output
            # Should contain separator in ID3v2.3 (// has highest priority)
            assert "//" in raw_output
