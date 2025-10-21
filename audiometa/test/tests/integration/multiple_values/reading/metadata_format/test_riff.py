
from audiometa import get_specific_metadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.riff.riff_metadata_setter import RIFFMetadataSetter
from audiometa.test.helpers.riff.riff_metadata_getter import RIFFMetadataGetter


class TestRiff:
    
    def test_semicolon_separated_artists(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_artists(test_file.path, ["Artist One;Artist Two;Artist Three"], in_separate_frames=False)
                        
            verification = RIFFMetadataGetter.get_raw_metadata(test_file.path, "IART")
            assert "Artist                          : Artist One;Artist Two;Artist Three" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.RIFF)
            
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist One" in artists
            assert "Artist Two" in artists
            assert "Artist Three" in artists

    def test_multiple_artists_in_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_artists(test_file.path, ["One", "Two", "Three"], in_separate_frames=True)
            
            verification_result = RIFFMetadataGetter.get_raw_metadata(test_file.path, "IART")
            
            assert verification_result["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification_result['actual_count']}"
            
            # Get RIFF metadata specifically to read the artists
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.RIFF)

            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "One" in artists
            assert "Two" in artists
            assert "Three" in artists
            
    def test_mixed_separators_and_multiple_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_artists(test_file.path, ["Artist 1;Artist 2", "Artist 3", "Artist 4"], in_separate_frames=True)

            verification = RIFFMetadataGetter.get_raw_metadata(test_file.path, "IART")

            # Verify the raw data creation - exiftool shows RIFF tags as "Artist" not "IART"
            assert verification["actual_count"] == 3, f"Expected 3 separate IART frames, found {verification['actual_count']}"
            assert "[RIFF]" in verification['raw_output']
            assert "Artist" in verification['raw_output']
            assert "Artist 1;Artist 2" in verification['raw_output'] 
            assert "Artist 3" in verification['raw_output']
            assert "Artist 4" in verification['raw_output']
            
            # Get RIFF metadata specifically to read the artists
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS, metadata_format=MetadataFormat.RIFF)
            assert isinstance(artists, list)
            
            # We created 3 separate RIFF frames, so we should get 3 entries 
            # (separator parsing happens at a higher level, not in RIFF format itself)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists
            
    def test_multiple_title_entries_then_first_one(self):
        with TempFileWithMetadata({"title": "Test Song"}, "wav") as test_file:
            RIFFMetadataSetter.set_multiple_titles(test_file.path, ["Title One", "Title Two", "Title Three"], in_separate_frames=True)
            
            verification = RIFFMetadataGetter.get_raw_metadata(test_file.path, "INAM")

            assert verification["actual_count"] == 3, f"Expected 3 separate INAM frames, found {verification['actual_count']}"
            assert "Title One" in verification['raw_output']
            assert "Title Two" in verification['raw_output']
            assert "Title Three" in verification['raw_output']
            
            title = get_specific_metadata(test_file.path, UnifiedMetadataKey.TITLE, metadata_format=MetadataFormat.RIFF)
            assert isinstance(title, str)
            assert title == "Title One"