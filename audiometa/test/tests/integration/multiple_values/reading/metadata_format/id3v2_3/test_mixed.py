from audiometa import get_merged_unified_metadata, get_specific_metadata, update_file_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.MetadataFormat import MetadataFormat
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


class TestId3v23Mixed:
    def test_mixed_single_and_multiple_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_artists(["Artist 1;Artist 2", "Artist 3", "Artist 4"], version="2.3")
            verification = test_file.verify_id3v2_multiple_entries_in_raw_data("TPE1", expected_count=3)
            
            assert "TPE1" in verification['raw_output'] 
            assert "Artist 1;Artist" in verification['raw_output']
            assert "Artist 3" in verification['raw_output']
            assert "Artist 4" in verification['raw_output']
            
            artists = get_specific_metadata(test_file.path, UnifiedMetadataKey.ARTISTS_NAMES)
            assert isinstance(artists, list)
            assert len(artists) == 3
            assert "Artist 1;Artist 2" in artists
            assert "Artist 3" in artists
            assert "Artist 4" in artists

    def test_mixed_genres_no_parsing(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres(["Rock;Alternative", "Indie", "Electronic"], version="2.3")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            assert isinstance(genres, list)
            assert len(genres) == 3
            assert "Rock;Alternative" in genres
            assert "Indie" in genres
            assert "Electronic" in genres

    def test_mixed_composers_preserves_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_composers(["John Doe;Jane Smith", "Bob Wilson", "Alice Cooper"], version="2.3")
            
            composers = get_specific_metadata(test_file.path, UnifiedMetadataKey.COMPOSER)
            assert isinstance(composers, list)
            assert len(composers) == 3
            assert "John Doe;Jane Smith" in composers
            assert "Bob Wilson" in composers
            assert "Alice Cooper" in composers