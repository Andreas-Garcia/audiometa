from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_inspector import ID3v2MetadataInspector
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter


class TestMultipleEntriesId3v2_4:
    def test_write_multiple_artists(self, temp_audio_file: Path):
        metadata = {
            UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
        }
        
        update_file_metadata(temp_audio_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
        
        verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(temp_audio_file, "TPE1")
        assert verification['success']
        # In ID3v2.4, multiple artists should be in a single frame with null separators (per spec)
        raw_output = verification['raw_output']
        assert raw_output in ["TPE1=Artist One\0Artist Two", "TPE1=Artist Two\0Artist One"]

    def test_write_on_existing_artists_field(self, temp_audio_file: Path):
        # Start with an existing artist field
        initial_metadata = {"artist": "Existing Artist"}
        with TempFileWithMetadata(initial_metadata, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_artist(test_file.path, "Existing A\0Existing B", version="2.4")
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            raw_output = verification['raw_output']
            assert "TPE1=Existing A\0Existing B" in raw_output
            
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Existing A", "New B"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            verification = ID3v2MetadataInspector.inspect_multiple_entries_in_raw_data(test_file.path, "TPE1")
            assert verification['success']
            raw_output = verification['raw_output']
            assert "Existing A" in raw_output
            assert "New B" in raw_output
            # Should contain null separator in ID3v2.4
            assert "\0" in raw_output