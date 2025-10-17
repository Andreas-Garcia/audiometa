import pytest

from audiometa import get_merged_unified_metadata, get_specific_metadata
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.utils.MetadataFormat import MetadataFormat

@pytest.mark.integration
class TestVorbisGenreReading:

    def test_vorbis_single_genre(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_vorbis_multiple_genres_separate_entries(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_semicolon_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_comma_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Jazz, Fusion, Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Jazz", "Fusion", "Experimental"]

    def test_vorbis_genre_with_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Electronic/Dance/Ambient")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Electronic", "Dance", "Ambient"]

    def test_vorbis_genre_with_double_slash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock//Alternative//Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock\\Alternative\\Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_with_double_backslash_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock\\\\Alternative\\\\Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_mixed_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; Alternative; Indie; Experimental")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie", "Experimental"]

    def test_vorbis_genre_with_extra_whitespace(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre(" Rock ; Alternative ; Indie ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_duplicate_separators(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock;;;Alternative")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_vorbis_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None

    def test_vorbis_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # For None values, we don't set any genre metadata
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_vorbis_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("   ")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None

    def test_vorbis_genre_special_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock & Roll; R&B; Hip-Hop")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock & Roll", "R&B", "Hip-Hop"]

    def test_vorbis_genre_unicode_characters(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Música; 音楽; موسيقى")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Música", "音楽", "موسيقى"]

    def test_vorbis_genre_very_long_text(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            long_genre = "Very Long Genre Name That Might Exceed Normal Limits And Test Edge Cases For Vorbis Format In FLAC Files"
            test_file.set_vorbis_genre(long_genre)
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == [long_genre]

    def test_vorbis_genre_custom_genre_names(self):
        custom_genres = [
            "Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave",
            "Synthwave", "Retrowave", "Outrun", "Future Funk", "Lo-Fi Hip Hop",
            "Ambient", "Drone", "Noise", "Experimental", "Avant-garde"
        ]
        
        for genre in custom_genres:
            with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
                test_file.set_vorbis_genre(genre)
                
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
                
                assert genres == [genre]

    def test_vorbis_genre_multiple_custom_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            custom_genres = ["Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave", "Ambient", "Drone"]
            test_file.set_vorbis_genre("; ".join(custom_genres))
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == custom_genres

    def test_vorbis_genre_no_genre_codes_support(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("17; 20; 131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_vorbis_genre_text_based_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; Alternative; Indie")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_vorbis_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []

    def test_vorbis_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Title", "artist": "Test Artist", "album": "Test Album"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; Alternative; Indie")
            
            metadata = get_merged_unified_metadata(test_file.path)
            genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]
            assert metadata.get(UnifiedMetadataKey.TITLE) == "Test Title"
            assert metadata.get(UnifiedMetadataKey.ARTISTS_NAMES) == ["Test Artist"]
            assert metadata.get(UnifiedMetadataKey.ALBUM_NAME) == "Test Album"

    def test_vorbis_genre_edge_case_single_character(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("A")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["A"]

    def test_vorbis_genre_edge_case_numbers_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("12345")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["12345"]

    def test_vorbis_genre_edge_case_special_separators_in_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock with semicolons; Another, with, commas; Rock/with/slashes")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock with semicolons", "Another, with, commas", "Rock/with/slashes"]

    def test_vorbis_genre_utf8_encoding(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Música Electrónica; 電子音楽; موسيقى إلكترونية")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Música Electrónica", "電子音楽", "موسيقى إلكترونية"]

    def test_vorbis_genre_mixed_languages(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            test_file.set_vorbis_genre("Rock; ロック; Roc; Рок")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "ロック", "Roc", "Рок"]

    def test_vorbis_genre_very_many_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            many_genres = [f"Genre {i}" for i in range(50)]
            test_file.set_vorbis_genre("; ".join(many_genres))
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == many_genres

    def test_vorbis_genre_empty_list(self):
        with TempFileWithMetadata({"title": "Test Song"}, "flac") as test_file:
            # For empty list, we don't set any genre metadata
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres is None or genres == []
