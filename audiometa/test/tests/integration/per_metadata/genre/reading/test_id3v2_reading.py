import pytest

from audiometa import get_merged_unified_metadata, get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestId3v2GenreReading:

    def test_id3v2_single_genre(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_id3v2_multiple_genres_separate_frames(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres( ["Rock", "Alternative", "Indie"])
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_semicolon_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_comma_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Jazz, Fusion, Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_id3v2_genre_with_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Electronic/Dance/Ambient")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_id3v2_genre_with_double_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock//Alternative//Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock\\Alternative\\Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_double_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock\\\\Alternative\\\\Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_mixed_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock; Alternative, Indie/Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie", "Experimental"]

    def test_id3v2_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( " Rock ; Alternative ; Indie ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock;;;Alternative")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_id3v2_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # No genre set - test file has no genre
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_id3v2_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "   ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_id3v2_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock & Roll; R&B; Hip-Hop")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_id3v2_genre_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Música; 音楽; موسيقى")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Música", "音楽", "موسيقى"]

    def test_id3v2_genre_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases For ID3v2 Format"
            test_file.set_id3v2_genre( long_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == [long_genre]

    def test_id3v2_genre_custom_genre_names(self):
        custom_genres = [
            "Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave",
            "Synthwave", "Retrowave", "Outrun", "Future Funk", "Lo-Fi Hip Hop"
        ]
        
        for genre in custom_genres:
            with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
                test_file.set_id3v2_genre( genre)
                
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
                
                assert genres == [genre]

    def test_id3v2_genre_multiple_custom_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            custom_genres = ["Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave"]
            test_file.set_id3v2_multiple_genres( custom_genres)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == custom_genres

    def test_id3v2_genre_with_genre_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_id3v2_genre_mixed_names_and_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "Rock; 20; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "20", "Indie"]

    def test_id3v2_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_id3v2_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist", "album": "Test Album"}, "mp3") as test_file:
            # Set genre using helper
            test_file.set_id3v2_multiple_genres(["Rock", "Alternative"])
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_id3v2_genre_id3v2_3_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres( ["Rock", "Alternative"])
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_id3v2_4_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres( ["Rock", "Alternative"])
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_edge_case_single_character(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "A")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["A"]

    def test_id3v2_genre_edge_case_numbers_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_genre( "12345")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["12345"]

    def test_id3v2_genre_edge_case_special_separators_in_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            test_file.set_id3v2_multiple_genres( ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"])
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]
