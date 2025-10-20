import pytest

from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestRiff:
    
    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_separator_artists("Artist One;Artist Two;Artist Three")
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.RIFF)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_multiple_artists_unified_reading(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["One", "Two", "Three"], in_separate_frames=True)
            
            # Verify that artists are actually stored in separate RIFF frames
            verification_result = test_file.verify_riff_multiple_entries_in_raw_data("IART", expected_count=3)
            
            assert verification_result["success"], f"Verification failed: {verification_result.get('error', 'Unknown error')}"
            assert verification_result["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification_result['actual_count']}"
            
            # Get RIFF metadata specifically to read the artists
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.RIFF)

            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
            
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"], in_separate_frames=True)
            verification = test_file.verify_riff_multiple_entries_in_raw_data("IART", expected_count=3)
            
            # Verify the raw data creation - exiftool shows RIFF tags as "Artist" not "IART"
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert verification["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification['actual_count']}"
            assert "[RIFF]" in verification['raw_output']
            assert "Artist" in verification['raw_output']
            assert "Artist 1;Artist 2" in verification['raw_output'] 
            assert "Artist 3" in verification['raw_output']
            assert "Artist 4" in verification['raw_output']
            
            # Get RIFF metadata specifically to read the artists
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.RIFF)
            assert isinstance(artists, list)
            
            # We created 3 separate RIFF frames, so we should get 3 entries 
            # (separator parsing happens at a higher level, not in RIFF format itself)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists
            
    def test_multiple_title_entries_then_first_one(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            test_file.set_riff_multiple_titles(["Title One", "Title Two", "Title Three"])
            verification = test_file.verify_riff_multiple_entries_in_raw_data("INAM", expected_count=3)
            
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert verification["actual_count"] == 3, f"Expected 3 separate INAM frames, found {verification['actual_count']}"
            assert "Title One" in verification['raw_output']
            assert "Title Two" in verification['raw_output']
            assert "Title Three" in verification['raw_output']
            
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.RIFF)
            assert isinstance(title, str)
            assert title == "Title One"