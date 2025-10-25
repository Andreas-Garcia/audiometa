import pytest

from audiometa import get_unified_metadata, get_unified_metadata_field
from audiometa.test.helpers.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.helpers.id3v2 import ID3v2MetadataSetter
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey


@pytest.mark.integration
class TestId3v2GenreReading:

    def test_id3v2_single_genre(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genre(test_file.path, "Rock")
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock"]

    def test_id3v2_multiple_genres_separate_frames(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock", "Alternative", "Indie"])
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_with_semicolon_separator(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genre(test_file.path, "Rock; Alternative; Indie")
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative", "Indie"]

    def test_id3v2_genre_custom_genre_names(self):
        custom_genres = [
            "Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave",
            "Synthwave", "Retrowave", "Outrun", "Future Funk", "Lo-Fi Hip Hop"
        ]
        
        for genre in custom_genres:
            with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
                ID3v2MetadataSetter.set_genre(test_file.path, genre)
                
                metadata = get_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRES_NAMES)
                
                assert genres == [genre]

    def test_id3v2_genre_multiple_custom_genres(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            custom_genres = ["Post-Rock", "Shoegaze", "Dream Pop", "Chillwave", "Vaporwave"]
            ID3v2MetadataSetter.set_genres(test_file.path, custom_genres)
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == custom_genres

    def test_id3v2_genre_with_genre_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genre(test_file.path, "17; 20; 131")
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["17", "20", "131"]

    def test_id3v2_genre_mixed_names_and_codes(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genre(test_file.path, "Rock; 20; Indie")
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "20", "Indie"]

    def test_id3v2_genre_id3v2_3_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock", "Alternative"])
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_id3v2_4_version(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock", "Alternative"])
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock", "Alternative"]

    def test_id3v2_genre_edge_case_numbers_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genre(test_file.path, "12345")
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["12345"]

    def test_id3v2_genre_edge_case_special_separators_in_values(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ID3v2MetadataSetter.set_genres(test_file.path, ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"])
            
            genres = get_unified_metadata_field(test_file.path, UnifiedMetadataKey.GENRES_NAMES)
            
            assert genres == ["Rock; with; semicolons", "Another, with, commas", "Rock/with/slashes"]
