

from audiometa import get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3HeaderVerifier
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v23:
    
    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_separator_artists("Artist One;Artist Two;Artist Three", version="2.3")
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            verification = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=1)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert "TPE1=Artist One;Artist Two;Artist Three" in verification['raw_output']

            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)

            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
    def test_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["One", "Two", "Three"], version="2.3", in_separate_frames=True)
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            verification = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=3)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
            
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"], version="2.3", in_separate_frames=True)
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            verification = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=3)
            
            assert "TPE1" in verification['raw_output'] 
            assert "Artist 1;Artist" in verification['raw_output']
            assert "Artist 3" in verification['raw_output']
            assert "Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists
            
    def test_multiple_title_entries_then_first_one(self):
        with TempFileWithMetadata({"title": "Initial Title"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_titles(["Title One", "Title Two", "Title Three"], version="2.3", in_separate_frames=True)
            
            assert ID3HeaderVerifier.get_id3v2_version(test_file.path) == (2, 3, 0)
            
            verification = test_file.verify_id3v2_multiple_entries_in_raw_data("TIT2", expected_count=3)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            
            titles = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(titles, list)
            assert len(titles) == 3
            assert "Title One" in titles
            assert "Title Two" in titles
            assert "Title Three" in titles