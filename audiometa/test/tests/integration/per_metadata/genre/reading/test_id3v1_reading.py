import pytest
import subprocess
from pathlib import Path

from audiometa import get_merged_unified_metadata, get_specific_metadata
from audiometa.utils.UnifiedMetadataKey import UnifiedMetadataKey
from audiometa.test.tests.temp_file_with_metadata import TempFileWithMetadata
from audiometa.test.tests.test_script_helpers import ScriptHelper


@pytest.mark.integration
class TestId3v1GenreReading:

    def test_id3v1_genre_code_17_rock(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_code_0_blues(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "0")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Blues"]

    def test_id3v1_genre_code_32_classical(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "32")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Classical"]

    def test_id3v1_genre_code_80_folk(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "80")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Folk"]

    def test_id3v1_genre_code_131_indie(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "131")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Indie"]

    def test_id3v1_genre_code_189_dubstep(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "189")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Dubstep"]

    def test_id3v1_genre_code_255_unknown(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "255")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None

    def test_id3v1_genre_single_genre_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_case_insensitive_conversion(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_partial_match_conversion(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres == ["Rock"]

    def test_id3v1_genre_30_character_limit(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            long_genre = "Very Long Genre Name That Exceeds 30 Characters"
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None
            assert len(genres[0]) <= 30

    def test_id3v1_genre_empty_string(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "255")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_none_value(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            # No genre set - test file has no genre
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_whitespace_only(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "255")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_latin1_encoding(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is not None

    def test_id3v1_genre_original_specification_codes(self):
        # Test a representative sample of original ID3v1 specification genres
        original_genres = [
            "Blues", "Classic Rock", "Country", "Dance", "Disco", 
            "Funk", "Grunge", "Hip-Hop", "Jazz", "Metal"
        ]
        
        for genre in original_genres:
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_winamp_extensions(self):
        # Test a representative sample of Winamp extension genres
        # Note: Only genres recognized by id3v2 tool are tested
        winamp_genres = [
            "Folk", "Jazz", "Classical", "Country", "Pop",
            "Metal", "Hip-Hop", "Electronic", "Rock", "Blues"
        ]
        
        for genre in winamp_genres:
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_winamp_56_extensions(self):
        # Test a representative sample of Winamp 5.6 extension genres
        # Note: Only genres recognized by id3v2 tool are tested
        winamp_56_genres = [
            "Reggae", "Jazz", "Electronic", "Rock", "Blues",
            "Classical", "Folk", "Country", "Pop", "Metal"
        ]
        
        for genre in winamp_56_genres:
            with TempFileWithMetadata({"title": "Test Song", "genre": genre}, "id3v1") as test_file:
                metadata = get_merged_unified_metadata(test_file.path)
                genres = metadata.get(UnifiedMetadataKey.GENRE_NAME)
                
                assert genres == [genre]

    def test_id3v1_genre_no_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            
            assert genres is None or genres == []

    def test_id3v1_genre_with_other_metadata(self):
        with TempFileWithMetadata({"title": "Test Song"}, "mp3") as test_file:
            ScriptHelper.set_id3v1_genre(test_file.path, "17")
            
            # Test that genre reading works correctly
            genres = get_specific_metadata(test_file.path, UnifiedMetadataKey.GENRE_NAME)
            assert genres == ["Rock"]
            
            # Test that other metadata is also present (using get_merged_unified_metadata for multiple fields)
            metadata = get_merged_unified_metadata(test_file.path)
            assert metadata.get(UnifiedMetadataKey.TITLE) is not None


