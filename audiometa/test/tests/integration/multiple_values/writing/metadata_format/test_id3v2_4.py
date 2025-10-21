from pathlib import Path

from audiometa import update_file_metadata, get_merged_unified_metadata, get_single_format_app_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2.id3v2_metadata_getter import ID3v2MetadataGetter
from audiometa.test.helpers.id3v2.id3v2_metadata_setter import ID3v2MetadataSetter


class TestMultipleEntriesId3v2_4:
    def test_write_multiple_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Artist One", "Artist Two"]
            }
            
            update_file_metadata(test_file, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            verification = {'raw_output': raw_metadata.get("TPE1", "")}
            raw_output = verification['raw_output']
            
            # raw_output replaces NUL bytes with slashes for display purposes
            assert "TPE1=Artist One / Artist Two" in raw_output or "TPE1=Artist One / Artist Two" in raw_output

    def test_write_on_existing_artists_field(self):
        initial_metadata = {"artist": "Existing Artist"}
        with TempFileWithMetadata(initial_metadata, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_artist(test_file.path, "Existing A\0Existing B", version="2.4")
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            verification = {'raw_output': raw_metadata.get("TPE1", "")}
            raw_output = verification['raw_output']
            
            # raw_output replaces NUL bytes with slashes for display purposes
            assert "TPE1=Existing A / Existing B" in raw_output
            
            metadata = {
                UnifiedMetadataKey.ARTISTS_NAMES: ["Existing A", "New B"]
            }
            update_file_metadata(test_file.path, metadata, metadata_format=MetadataFormat.ID3V2, id3v2_version=(2, 4, 0))
            
            raw_metadata = ID3v2MetadataGetter.get_raw_metadata(test_file.path)
            verification = {'raw_output': raw_metadata.get("TPE1", "")}
            raw_output = verification['raw_output']
            assert "Existing A" in raw_output
            assert "New B" in raw_output
            # Should contain null separator in ID3v2.4
            assert " / " in raw_output