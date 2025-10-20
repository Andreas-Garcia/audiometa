
from audiometa import get_specific_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter, ID3v2MetadataVerifier, ID3V2HeaderVerifier


class TestId3v2_4Mixed:

    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_artist(test_file.path, "Artist One;Artist Two;Artist Three", version="2.4")
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(test_file.path, "TPE1", expected_count=1)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert "TPE1=Artist One;Artist Two;Artist Three" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
        

    def test_multiple_artists_in_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_artists(test_file.path, ["Artist One", "Artist Two", "Artist Three"], in_separate_frames=False, version="2.4")
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(test_file.path, "TPE1", expected_count=3)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            assert "TPE1=Artist One / Artist Two / Artist Three" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists
            
            
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"], version="2.4")
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)
            
            verification = ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(test_file.path, "TPE1", expected_count=3)
            
            assert "TPE1=Artist 1;Artist 2 / Artist 3 / Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES, metadata_format=MetadataFormat.ID3V2)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists
            
    def test_multiple_title_entries_then_first_one(self):
        with TempFileWithMetadata({"title": "Test Song"}, "id3v2.4") as test_file:
            ID3v2MetadataSetter.set_titles(test_file.path, ["Title One", "Title Two", "Title Three"], in_separate_frames=True, version="2.4")
            
            assert ID3V2HeaderVerifier.get_id3v2_version(test_file.path) == (2, 4, 0)

            verification = ID3v2MetadataVerifier.verify_multiple_entries_in_raw_data(test_file.path, "TIT2", expected_count=3)
            assert verification["success"], f"Verification failed: {verification.get('error', 'Unknown error')}"
            
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.ID3V2)
            
            assert isinstance(title, str)
            assert title == "Title One"